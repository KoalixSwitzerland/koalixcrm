#!/usr/bin/env python3
"""
Pre-migration preparation for upgrading from the old monolithic CRM.

Run this BEFORE `python manage.py migrate` when upgrading from the old
PostgreSQL-based app to the new split-app SQLite structure.

Strategy:
1. Extract all data from the old (pg2sqlite-converted) database
2. Drop all tables so Django can recreate them with proper schemas
3. Keep only non-koalix Django tables (admin, auth, contenttypes, sessions)
   intact via data preservation
4. After this script, run `python manage.py migrate` to create proper tables,
   then run the data import step.

Safe to run on fresh installs (no-op) and idempotent on upgrades.
"""

import json
import os
import sys
import sqlite3


def extract_data(db_path, dump_path):
    """Extract all row data from the database into a JSON file."""
    if not os.path.exists(db_path):
        print(f"No database found at {db_path} - fresh install.")
        return False

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Check if this is a legacy database
    cursor.execute(
        "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='django_migrations'"
    )
    if cursor.fetchone()[0] == 0:
        print("No django_migrations table - fresh install.")
        conn.close()
        return False

    cursor.execute(
        "SELECT COUNT(*) FROM django_migrations WHERE app = 'crm' AND name = '0002_auto_20170927_2042'"
    )
    is_upgrade = cursor.fetchone()[0] > 0
    if not is_upgrade:
        print("No legacy migration records found - not a legacy database.")
        conn.close()
        return False

    print("Detected legacy database. Extracting data...")

    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = [row[0] for row in cursor.fetchall()
              if not row[0].startswith('sqlite_')]

    data = {}
    for table in tables:
        cursor.execute(f'SELECT * FROM "{table}"')
        columns = [desc[0] for desc in cursor.description]
        rows = [list(row) for row in cursor.fetchall()]
        if rows:
            data[table] = {'columns': columns, 'rows': rows}
            print(f"  Extracted {len(rows)} rows from {table}")

    with open(dump_path, 'w') as f:
        json.dump(data, f)

    conn.close()
    print(f"Data saved to {dump_path}")
    return True


def drop_all_tables(db_path):
    """Drop all tables so Django can recreate them with proper schemas."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = [row[0] for row in cursor.fetchall()
              if not row[0].startswith('sqlite_')]

    # Disable foreign key checks during drop
    cursor.execute("PRAGMA foreign_keys = OFF")
    for table in tables:
        cursor.execute(f'DROP TABLE IF EXISTS "{table}"')
        print(f"  Dropped {table}")

    conn.commit()
    conn.close()
    print("All tables dropped.")


def import_data(db_path, dump_path):
    """Import data back into Django-created tables."""
    if not os.path.exists(dump_path):
        print(f"No data dump found at {dump_path}")
        return

    with open(dump_path, 'r') as f:
        data = json.load(f)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = OFF")

    # Get existing tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    existing_tables = {row[0] for row in cursor.fetchall()}

    # Tables to skip during import (Django will populate these fresh)
    skip_tables = {
        'django_migrations',
        'django_content_type',
        'auth_permission',
        'south_migrationhistory',
    }

    total_imported = 0
    for table, table_data in data.items():
        if table in skip_tables:
            print(f"  Skipped {table} (will be populated by Django)")
            continue

        if table not in existing_tables:
            print(f"  Skipped {table} (table does not exist in new schema)")
            continue

        columns = table_data['columns']
        rows = table_data['rows']

        # Get actual columns in the new table
        cursor.execute(f'PRAGMA table_info("{table}")')
        new_columns = {row[1] for row in cursor.fetchall()}

        # Filter to only columns that exist in the new table
        col_indices = []
        valid_columns = []
        for i, col in enumerate(columns):
            if col in new_columns:
                col_indices.append(i)
                valid_columns.append(col)
            else:
                print(f"  Note: column '{col}' in {table} not in new schema, skipping")

        if not valid_columns:
            continue

        col_names = ', '.join(f'"{c}"' for c in valid_columns)
        placeholders = ', '.join(['?'] * len(valid_columns))
        sql = f'INSERT OR IGNORE INTO "{table}" ({col_names}) VALUES ({placeholders})'

        filtered_rows = [[row[i] for i in col_indices] for row in rows]

        try:
            cursor.executemany(sql, filtered_rows)
            total_imported += len(filtered_rows)
            print(f"  Imported {len(filtered_rows)} rows into {table}")
        except Exception as e:
            print(f"  ERROR importing {table}: {e}")
            # Try row by row
            imported = 0
            for row in filtered_rows:
                try:
                    cursor.execute(sql, row)
                    imported += 1
                except Exception:
                    pass
            if imported:
                total_imported += imported
                print(f"    Imported {imported}/{len(filtered_rows)} rows individually")

    conn.commit()
    conn.close()
    print(f"\nTotal: imported {total_imported} rows")


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, 'projectsettings', 'db.sqlite3')
    dump_path = os.path.join(base_dir, 'projectsettings', 'legacy_data.json')

    if len(sys.argv) > 1:
        db_path = sys.argv[1]
    if len(sys.argv) > 2:
        dump_path = sys.argv[2]

    command = sys.argv[-1] if len(sys.argv) > 1 and sys.argv[-1] in ('extract', 'import', 'prepare') else 'prepare'

    if command == 'extract':
        extract_data(db_path, dump_path)
    elif command == 'import':
        import_data(db_path, dump_path)
    elif command == 'prepare':
        # Full preparation: extract data, then drop all tables
        success = extract_data(db_path, dump_path)
        if success:
            drop_all_tables(db_path)
            print("\nNext steps:")
            print("  1. Run: python manage.py migrate")
            print("  2. Run: python koalixcrm_utils/pre_migrate_cleanup.py import")


if __name__ == '__main__':
    main()
