# -*- coding: utf-8 -*-
"""Reconcile django_migrations for legacy / mid-refactor deployments.

Legacy deployments (e.g. the 2019-era monolithic schema) and partially-
split deployments (post products app split, pre settings split) have
tables that today belong to a different migration. Django's
`check_consistent_history` runs at the start of every `migrate` and
refuses to proceed if an applied migration has an unapplied dependency in
the current graph.

This command walks the current migration graph and records any
`CreateModel`-style migration as applied when all the tables it would
create already exist. It's a generalised `--fake-initial` that isn't
limited to initial migrations, so it handles the chain of dependencies
that were re-organised during the products → settings split and earlier
splits from the monolithic `crm` app.

Safe to run on fresh databases: if tables don't exist, nothing is
recorded and normal `migrate` proceeds as usual. Idempotent on already-
current databases: migrations already recorded as applied are skipped.
"""

import re

from django.core.management.base import BaseCommand
from django.db import connection
from django.db.migrations.loader import MigrationLoader
from django.db.migrations.recorder import MigrationRecorder

CREATE_MODEL_OP_NAMES = ("CreateModel", "CreateModelIfNotExists")

# Matches legacy `id integer NOT NULL` column declarations that are missing
# `PRIMARY KEY` / AUTOINCREMENT. Case-insensitive, whitespace-tolerant.
LEGACY_ID_RE = re.compile(
    r'("?id"?)\s+integer\s+NOT\s+NULL(?!\s+PRIMARY)',
    flags=re.IGNORECASE,
)

# Matches legacy `<model>_ptr_id integer NOT NULL` column declarations in
# MTI-child tables (Customer/Supplier inherit from Contact; PurchaseOrder
# etc. inherit from SalesDocument). Django treats the `_ptr_id` column as
# both the PK and a FK to the parent table; pre-Django-1.9 schemas declared
# it without PRIMARY KEY, which makes every later schema edit blow up with
# `foreign key mismatch` because the FK target isn't a proper PK.
LEGACY_PTR_ID_RE = re.compile(
    r'("?\w+_ptr_id"?)\s+integer\s+NOT\s+NULL(?!\s+PRIMARY)',
    flags=re.IGNORECASE,
)


class Command(BaseCommand):
    help = "Reconcile django_migrations for legacy/mid-refactor deployments."

    def handle(self, *args, **options):
        recorder = MigrationRecorder(connection)
        self._upgrade_migrations_table_if_legacy()
        self._upgrade_legacy_id_columns()
        recorder.ensure_schema()
        applied = set(recorder.applied_migrations())
        present = set(connection.introspection.table_names())

        loader = MigrationLoader(connection, ignore_no_migrations=True)

        # Process in dependency order so parents get recorded before children,
        # which matters only for presentation (has_table checks aren't needed).
        for key in loader.graph.nodes:
            if key in applied:
                continue
            migration = loader.graph.nodes[key]
            app, name = key
            create_tables = self._tables_created_by(migration, app)
            if not create_tables:
                continue
            if not all(t in present for t in create_tables):
                continue
            self._record_applied(app, name)
            applied.add(key)

    def _upgrade_migrations_table_if_legacy(self):
        """Rebuild django_migrations if it uses the pre-Django-1.9 schema.

        Legacy deployments have an `id` column without auto-increment, which
        breaks Django's own `MigrationRecorder.record_applied()`. Rebuild the
        table with the modern schema, preserving existing rows.
        """
        if "django_migrations" not in connection.introspection.table_names():
            return
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT sql FROM sqlite_master WHERE type='table' "
                "AND name='django_migrations'"
            )
            row = cursor.fetchone()
        if not row:
            return
        sql = row[0] or ""
        # Modern schema has `id integer NOT NULL PRIMARY KEY AUTOINCREMENT`.
        if "AUTOINCREMENT" in sql.upper() or "PRIMARY KEY" in sql.upper():
            return
        self.stdout.write(
            "Legacy django_migrations schema detected — rebuilding with "
            "auto-increment id while preserving rows."
        )
        with connection.cursor() as cursor:
            cursor.execute("SELECT app, name, applied FROM django_migrations")
            rows = cursor.fetchall()
            cursor.execute("DROP TABLE django_migrations")
        # Let Django recreate the table with the modern schema.
        MigrationRecorder(connection).ensure_schema()
        with connection.cursor() as cursor:
            cursor.executemany(
                "INSERT INTO django_migrations (app, name, applied) "
                "VALUES (%s, %s, %s)",
                rows,
            )

    def _upgrade_legacy_id_columns(self):
        """SQLite-only: rebuild tables whose `id` isn't `INTEGER PRIMARY KEY`.

        Pre-Django-1.9 schemas declared `id integer NOT NULL` without making
        it an alias for ROWID. SQLite's `foreign_key_check` then rejects any
        new table that references such a table, which blocks later
        migrations from applying. Rebuild each affected table with an
        `INTEGER PRIMARY KEY AUTOINCREMENT` id column, preserving row data
        and indexes.
        """
        if connection.vendor != "sqlite":
            return
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT name, sql FROM sqlite_master "
                "WHERE type='table' AND sql IS NOT NULL"
            )
            tables = cursor.fetchall()
        for table_name, create_sql in tables:
            if table_name.startswith("sqlite_") or table_name == "django_migrations":
                continue
            if not self._needs_id_upgrade(table_name, create_sql):
                continue
            self._rebuild_sqlite_table(table_name, create_sql)

    def _needs_id_upgrade(self, table_name, create_sql):
        """True if the table is missing a proper INTEGER PRIMARY KEY column.

        Two shapes trigger a rebuild:
          1. `id integer NOT NULL` without PRIMARY KEY — the 2019-era
             monolithic schema for every root model.
          2. `<model>_ptr_id integer NOT NULL` without PRIMARY KEY — same
             era's MTI-child tables (Customer/Supplier, PurchaseOrder/…).
        """
        with connection.cursor() as cursor:
            cursor.execute(f'PRAGMA table_info("{table_name}")')
            cols = cursor.fetchall()  # cid, name, type, notnull, dflt_value, pk
        has_pk = any(c[5] for c in cols)
        if has_pk:
            return False
        id_col = next((c for c in cols if c[1].lower() == "id"), None)
        if id_col and (id_col[2] or "").strip().upper() == "INTEGER":
            return bool(LEGACY_ID_RE.search(create_sql))
        ptr_col = next(
            (c for c in cols if c[1].lower().endswith("_ptr_id")), None,
        )
        if ptr_col and (ptr_col[2] or "").strip().upper() == "INTEGER":
            return bool(LEGACY_PTR_ID_RE.search(create_sql))
        return False

    def _rebuild_sqlite_table(self, table_name, create_sql):
        new_create_sql, count = LEGACY_ID_RE.subn(
            "id INTEGER PRIMARY KEY AUTOINCREMENT", create_sql, count=1,
        )
        if count == 0:
            # No root-model id column — must be an MTI child with <x>_ptr_id.
            # Don't AUTOINCREMENT: the child's PK must equal the parent's id,
            # so it's populated by the ORM, not by SQLite.
            match = LEGACY_PTR_ID_RE.search(create_sql)
            if not match:
                return
            ptr_col_name = match.group(1).strip('"')
            new_create_sql = LEGACY_PTR_ID_RE.sub(
                f'{ptr_col_name} INTEGER PRIMARY KEY', create_sql, count=1,
            )
            count = 1
        if count == 0:
            return
        tmp_name = f"{table_name}__sync_split_tmp"
        tmp_create_sql = new_create_sql.replace(table_name, tmp_name, 1)
        self.stdout.write(
            f'Rebuilding "{table_name}" to use INTEGER PRIMARY KEY AUTOINCREMENT id.'
        )
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT sql FROM sqlite_master WHERE type='index' "
                "AND tbl_name=%s AND sql IS NOT NULL",
                [table_name],
            )
            index_sqls = [r[0] for r in cursor.fetchall()]

            cursor.execute("PRAGMA foreign_keys=OFF")
            try:
                cursor.execute(tmp_create_sql)
                cursor.execute(
                    f'INSERT INTO "{tmp_name}" SELECT * FROM "{table_name}"'
                )
                cursor.execute(f'DROP TABLE "{table_name}"')
                cursor.execute(
                    f'ALTER TABLE "{tmp_name}" RENAME TO "{table_name}"'
                )
                for isql in index_sqls:
                    try:
                        cursor.execute(isql)
                    except Exception as exc:  # pragma: no cover - legacy edge case
                        self.stdout.write(
                            self.style.WARNING(
                                f"Could not recreate index on {table_name}: {exc}"
                            )
                        )
            finally:
                cursor.execute("PRAGMA foreign_keys=ON")

    def _tables_created_by(self, migration, app_label):
        tables = []
        for op in migration.operations:
            if type(op).__name__ not in CREATE_MODEL_OP_NAMES:
                continue
            model_name = getattr(op, "name", None)
            if not model_name:
                continue
            options = dict(getattr(op, "options", None) or {})
            tables.append(options.get("db_table") or f"{app_label}_{model_name.lower()}")
        return tables

    def _record_applied(self, app, name):
        MigrationRecorder(connection).record_applied(app, name)
        self.stdout.write(self.style.SUCCESS(f"Recorded {app}.{name} as applied."))
