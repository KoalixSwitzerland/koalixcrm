# Migration guide: koalixcrm v1.14.0 → v2.0.0

## Audience

The next engineer who has to:

- ship the v2.0.0 release to an existing deployment, or
- perform a further app split / model move on top of what v2.0.0 started.

Read the "Idea" section first — the rest only makes sense once you have
the mental model.

## The idea

koalixcrm v1.x was a monolithic Django project: every business model
lived in a single app (historically `crm`). v2.0.0 completes a multi-step
refactor that breaks that monolith into focused apps:

```
contacts               Contact, Customer, Supplier, Person,
                       CustomerGroup, CustomerBillingCycle, Call,
                       postal/phone/email addresses
accounting             accounts, bookings, periods, product categories
core                   shared value objects (Currency, Unit, Tax,
                       CurrencyTransform, UnitTransform) +
                       cross-cutting infrastructure (PDFExportProcess,
                       timezone middleware, documents/, exceptions,
                       const, signals, locale, templates, static)
products               ProductType, Product, Price, ProductPrice,
                       CustomerGroupTransform
contract_object_management
                       Contract, CommercialDocument, Quote, Invoice,
                       DeliveryNote, PurchaseOrder, PaymentReminder, …
reporting              Project, Task, Agreement, Estimation, Resource,
                       ReportingPeriod, …
djangoUserExtension    DocumentTemplate family, TemplateSet,
                       UserExtension, TextParagraphInDocumentTemplate
```

The `crm` app is gone; its contents were split into `contacts` (the
contact domain) and `core` (the shared infrastructure). The former
`settings` app was renamed to `core` to avoid the naming collision with
`django.conf.settings`.

Two invariants let this refactor roll out without rewriting the data:

1. **`db_table` names are preserved.** The models now live in different
   apps, but every table keeps its legacy name (`crm_currency`,
   `crm_unit`, `crm_tax`, `crm_producttype`, `crm_salesdocument`, …).
   That means the underlying SQL schema is untouched across the split,
   and the data continues to live where it always did.

2. **Migrations use `CreateModelIfNotExists` / `AddFieldIfNotExists`.**
   See `koalixcrm/migration_utils.py`. These custom operations are
   schema-safe no-ops when the target already exists. That lets a "new"
   initial migration (e.g. `settings.0001_initial`) run against a
   legacy database without colliding with the table the monolith
   already created.

The migration graph is consistent for fresh installs because the split
migrations declare proper cross-app dependencies (e.g.
`products.0001_initial` depends on `settings.0001_initial`). The catch
— and the reason this document exists — is that legacy deployments have
a `django_migrations` table that does not know about those new
migrations. That is what the reconciliation tooling is for.

## What v2.0.0 contains

1. The `core` app (new in v2.0.0): owns the shared value objects
   (`Currency`, `Unit`, `Tax`, `CurrencyTransform`, `UnitTransform`) plus
   the cross-cutting infrastructure that used to live in `crm`:
   `PDFExportProcess`, the timezone middleware, `documents/pdf_export`,
   `exceptions`, `const`, `inlinemixin`, legacy HTML views, the
   reporting URL config, templates, static assets, and management
   commands.
2. The `contacts` app (new in v2.0.0): owns the contact domain split
   out of `crm` — `Contact`, `Customer`, `Supplier`, `Person`,
   `CustomerGroup`, `CustomerBillingCycle`, `Call`, and postal / phone /
   email addresses plus their admin / serializer / viewset.
3. `core.0001_initial`, `core.0002_transforms`,
   `core.0003_pdf_export_process_links`, and
   `core.0004_pdf_export_process` migrations. PDFExportProcess lives in
   its own migration (not `core.0001_initial`) so that
   `sync_split_migrations` can auto-record `core.0001_initial` on the
   legacy 2019-era DB, which has `crm_currency`/`crm_unit`/`crm_tax`
   but no `crm_pdfexportprocess`.
4. `contacts.0001_initial`, `contacts.0002_initial`,
   `contacts.0003_add_postaladdress_subdivision_code` migrations.
5. `core_api_py/` REST façade (renamed from the former
   `settings_api_py/`) and `contacts_api_py/` REST façade (renamed from
   the former `crm_api_py/`). URL routing in
   `projectsettings/urls.py` pulls value-object viewsets from
   `core_api_py` and contact viewsets from `contacts_api_py`.
6. `sync_split_migrations` management command (in
   `koalixcrm/core/management/commands/`) — the operator-facing tool
   that makes legacy databases consistent with the new migration graph.
7. Both Docker entrypoints (`docker/dev/entrypoint.sh`,
   `docker/prod/entrypoint.sh`) run `sync_split_migrations` before
   `migrate`.

## The upgrade path for operators

One command, idempotent, safe on fresh installs:

```
python manage.py sync_split_migrations
python manage.py migrate --noinput
```

This is exactly what the container entrypoints do. Running it a second
time is a no-op.

## What `sync_split_migrations` does (and why)

Source: `koalixcrm/settings/management/commands/sync_split_migrations.py`.

The command runs three steps, in order, before any schema changes from
`migrate`:

### 1. Rebuild `django_migrations` if it uses the pre-Django-1.9 schema

Very old SQLite deployments (pre-2016) have:

```sql
CREATE TABLE django_migrations (
    id INTEGER NOT NULL,        -- no PRIMARY KEY, no AUTOINCREMENT
    app TEXT NOT NULL,
    name TEXT NOT NULL,
    applied TEXT NOT NULL
)
```

Django's own `MigrationRecorder.record_applied()` tries
`Migration.objects.create(app=…, name=…)`, which inserts `NULL` for
`id` and fails with `NOT NULL constraint failed`. The command detects
this (no `PRIMARY KEY` / `AUTOINCREMENT` in the `CREATE TABLE` SQL),
drops the table, lets Django recreate it with the modern schema, and
reinserts every row.

### 2. Rebuild tables whose `id` column isn't `INTEGER PRIMARY KEY`

Same vintage: many tables were created with `id integer NOT NULL`
instead of `id INTEGER PRIMARY KEY AUTOINCREMENT`. In SQLite these are
different things — the former is *not* an alias for ROWID, and SQLite's
`PRAGMA foreign_key_check` rejects any new table that FK-references it.
That blocked `contract_object_management.0003_add_sales_document_media`
(and future FK-adding migrations) with
`foreign key mismatch - "crm_salesdocumentmedia" referencing
"crm_salesdocument"`.

For every SQLite table whose `CREATE TABLE` SQL matches
`id integer NOT NULL` (case-insensitive, whitespace-tolerant, no
`PRIMARY KEY` present), the command performs the standard SQLite 12-step
rebuild: `PRAGMA foreign_keys=OFF` → create `<table>__sync_split_tmp`
with `id INTEGER PRIMARY KEY AUTOINCREMENT` → `INSERT … SELECT *` →
drop original → rename temp → recreate indexes from `sqlite_master` →
`PRAGMA foreign_keys=ON`. Row id values are preserved.

This step is SQLite-only; PostgreSQL deployments never had this problem.

### 3. Record `django_migrations` entries for tables that already exist

Walk the current migration graph. For every migration that isn't
already recorded as applied, look at its `CreateModel` /
`CreateModelIfNotExists` operations. If every `db_table` those
operations would create is already present in the database, record the
migration as applied. This is a generalised `migrate --fake-initial`
that isn't restricted to initial migrations, so it handles the chain of
dependencies that crossed app boundaries during the split.

On a 2019-era monolithic database the output is:

```
Recorded core.0001_initial as applied.
Recorded core.0002_transforms as applied.
Recorded contacts.0001_initial as applied.
Recorded contacts.0002_initial as applied.
Recorded products.0001_initial as applied.
Recorded contract_object_management.0001_initial as applied.
Recorded contract_object_management.0002_initial as applied.
Recorded reporting.0001_initial as applied.
```

After that, `migrate` sees a consistent history and applies only the
genuinely new migrations — e.g.
`contacts.0003_add_postaladdress_subdivision_code`,
`core.0003_pdf_export_process_links`,
`core.0004_pdf_export_process`,
`contract_object_management.0003_add_sales_document_media`,
`djangoUserExtension.0002_documenttemplate_s3_file_fields`.
`core.0004_pdf_export_process` creates `crm_pdfexportprocess` on
legacy DBs that don't have it yet; on DBs already migrated past it the
`CreateModelIfNotExists` guard makes it a no-op.

## How to do further splits or moves

This is the reason this document matters. If you need to pull another
group of models out of an existing app — say, moving `Call` out of
`contacts` into its own app — do it like this:

1. **Keep the `db_table` name.** Set
   `class Meta: db_table = "crm_customerbillingcycle"` (or whatever the
   existing legacy name is). This is what makes the refactor transparent
   to the schema.

2. **Mirror the app layout.** Look at the `settings` app for the
   reference shape: `admin/`, `models/`, `views/`, `serializers/`,
   `factory/`, `signals/`, `migrations/`. Each concern is a separate
   file re-exported from `__init__.py`.

3. **Write the new app's `0001_initial` with `CreateModelIfNotExists`.**
   Copy the field definitions from the existing migration that created
   the table. Use the custom operations from `koalixcrm/migration_utils.py`
   so the migration is a safe no-op against legacy databases.

4. **Rewrite the donor app's migration.** Remove the moved operations
   from the donor app's migration(s) and add a dependency on the new
   app's initial migration. `CreateModelIfNotExists` elsewhere will
   prevent re-creation conflicts against existing databases.

5. **Handle circular dependencies by splitting migrations.** The
   `core` ↔ `products` split needed this: `CurrencyTransform` and
   `UnitTransform` reference `products.ProductType`, but
   `products.ProductType` references `core.Unit` and `core.Tax`.
   Solution: three migrations in order `core.0001_initial` (creates
   Currency/Unit/Tax) → `products.0001_initial` (creates ProductType et
   al.) → `core.0002_transforms` (creates CurrencyTransform /
   UnitTransform). If your split has the same shape, use the same
   pattern.

6. **Update every downstream FK string.** Grep the codebase for the old
   `"app.Model"` strings in FKs and migration files; replace them with
   the new app label. The previous split touched
   `contracts/models/*`, `reporting/models/*`, `djangoUserExtension/models/*`,
   their migrations, tests, factories, and serializers — expect similar
   scope.

6.1 **If you're pulling models out of a legacy-era app whose
   `db_table` prefix is `crm_`, keep the prefix.** Every Meta on the
   moved model must set `db_table = "crm_<modelname>"` explicitly, AND
   every `CreateModelIfNotExists` in the new migration must include
   `'db_table': 'crm_<modelname>'` in its `options`. Otherwise
   `sync_split_migrations` will compare against the Django-inferred
   `<app>_<modelname>` and skip the migration on legacy DBs, and
   `makemigrations` will generate a phantom `AlterModelTable` migration
   renaming the legacy tables.

7. **Update the API surface if applicable.** v2.0.0 introduced
   `core_api_py` as a dedicated REST façade for core-owned entities
   (renamed from `settings_api_py`) and `contacts_api_py` as the
   contact-domain façade (renamed from `crm_api_py`). If your split has
   a client-facing REST surface, mirror that: move the viewsets, DTOs,
   and client methods to a new `<app>_api_py` package, and update
   `projectsettings/urls.py` routes to import from it.

8. **`sync_split_migrations` will keep working automatically.** The
   command walks the graph dynamically — it doesn't hard-code app
   names. As long as step 3 uses `CreateModelIfNotExists`, the new
   migration will be recorded as applied on legacy databases without
   any change to the command.

9. **Verify on a copy of the legacy DB.** The reference databases are
   in `/app/koalixcrm_data/db/`:
   - `auftraegekoalixnet_20230101.sqlite3` — 2019-era monolithic schema,
     the hardest case. If this migrates cleanly, most deployments will.
   - `olddb.sqlite3` — post-products-split, pre-settings-split.
   Workflow:
   ```
   cp /app/koalixcrm_data/db/auftraegekoalixnet_20230101.sqlite3 /tmp/test.sqlite3
   DJANGO_SETTINGS_MODULE=projectsettings.settings.development_docker_sqlite_settings \
     python manage.py sync_split_migrations     # point DATABASES at /tmp/test.sqlite3
   DJANGO_SETTINGS_MODULE=projectsettings.settings.development_docker_sqlite_settings \
     python manage.py migrate --noinput
   ```
   Then spot-check row counts against the original. Re-run
   `sync_split_migrations` and `migrate` a second time — both must be
   no-ops.

## Upgrading contacts data to the Party model

In addition to splitting the monolith, v2.0.0 restructures `Contact`,
`Customer`, `Supplier`, `Person`, `CustomerGroup`, and the
postal / phone / email satellite tables into a single **Party data
model** (ADR 0001 in `koalixcrm-system`, and
`PLAN_contact_party_data_model.md`). This is a one-way, data-preserving
migration. The v2.0.0 migration graph runs three phases in order:

1. **Create** the new Party tables (`contacts.0004_party_data_model`).
   Additive, empty rows, no legacy impact.
2. **Copy** every legacy row into the new tables
   (`contacts.0005_backfill_party`). Legacy tables are still
   authoritative; new tables mirror them.
3. **Verify** every invariant holds before the destructive step
   (`contacts.0006_verify_ready_for_cutover`). If any count mismatches,
   the verify migration raises `BackfillVerificationError` and `migrate`
   aborts *before* any legacy table is dropped.
4. **Drop** the legacy tables + FK columns (later migrations in #395).

Step 3 is the last chance to catch data issues while both sides of the
mapping still exist. On a healthy DB it's a ~100-ms read-only sweep;
on an unhealthy DB it prints a list of remediation hints and refuses
to proceed.

### Dry-run the migration on a DB copy before deploying

**Never** upgrade production without running this on a copy first:

```
cp /path/to/production.sqlite3 /tmp/test.sqlite3
# …point DATABASES at /tmp/test.sqlite3…
python manage.py migrate contacts 0005_backfill_party    # up to backfill
python manage.py contacts_backfill_reconcile             # run every invariant

# If the reconcile exits 0, go ahead:
python manage.py migrate                                  # runs the rest
```

`contacts_backfill_reconcile` runs the same verifier as the migration,
but as a standalone command — so it's safe to invoke repeatedly while
diagnosing, and it prints a full table of every invariant (passed and
failed) before exiting with the appropriate status code.

### What the verify step checks

| # | Invariant | Why it matters |
|---|---|---|
| 1 | `Party.count == legacy Contact.count + legacy Person.count` | Every legacy row produced exactly one new Party. |
| 2 | `Organization.count == legacy Contact.count` | Every org-like legacy Contact became an Organization. |
| 3 | `PartyContact.count == legacy Person.count` | Every legacy Person became a natural-person Party. |
| 4 | `PartyRole(customer).count == legacy Customer.count` | Every legacy Customer has an active customer role. |
| 5 | `PartyRole(supplier).count == legacy Supplier.count` | Every legacy Supplier has an active supplier role. |
| 6 | `OrganizationMembership.count == legacy ContactPersonAssociation.count` | Every person-at-company link is preserved. |
| 7 | `AddressAssignment.count >= legacy PostalAddressForContact.count` | Every postal address migrated (`>=` because new addresses are dedup'd across parties). |
| 8 | `EmailAssignment.count >= legacy EmailAddressForContact.count + Person.email-having` | Same for emails (person.email promoted). |
| 9 | `PhoneAssignment.count >= legacy PhoneAddressForContact.count + Person.phone-having` | Same for phones. |
| 10 | `PartyGroup.count == legacy CustomerGroup.count` | Every legacy CustomerGroup became a PartyGroup. |
| 11 | Every `Contract` with `default_customer` has `buyer_party` set | FK rewire from v2.0.0 PR #394 phase A. |
| 12 | Every `Contract` with `default_supplier` has `supplier_party` set | Same. |
| 13 | Every `CommercialDocument` with `customer` has `party` set | Same — and `party` becomes NOT NULL right after. |
| 14 | Every `Price` with `customer_group` has `party_group` set | FK rewire from PR #394 phase B. |
| 15 | Every `CustomerGroupTransform` has both `from_/to_party_group` set | Same — NOT NULL right after. |

### What to do when a check fails

**Roll the DB copy back to v1.14.0 and fix the source data there.** The
backfill is deterministic; if the new Party tables are short, the
legacy tables had data the migration couldn't resolve — usually
orphans, duplicates, or `NULL` fields that v1.14.0 allowed but v2.0.0's
tighter constraints don't.

Concrete remediations per category of failure:

- **Count invariants (#1–#10) off by one-or-more.** Usually caused by:
  - *Orphan satellite rows* (e.g. a `PostalAddressForContact` whose
    `person_id` points at a Contact that was hard-deleted in the old
    admin). Fix: in v1.14.0 admin, either reassign the orphan to a
    valid Contact or delete it.
  - *Duplicate Customer / Supplier rows* for the same natural person.
    Fix: merge them in v1.14.0 admin (copy the satellites onto the
    survivor, delete the duplicates).
  - *Person rows that no longer belong to a Contact* (M2M cleared but
    Person kept around). Fix: delete the Person row if it's no longer
    used, or re-associate it with the correct Contact.
- **FK-rewire invariants (#11–#15) report "N legacy FKs, M−N < N new
  FKs".** The legacy FK points at a Customer / Supplier /
  CustomerGroup row that was *not* migrated into the new Party
  tables — usually because the source row was deleted between the
  backfill and the verify (which shouldn't happen within one `migrate`
  invocation). If this occurs on a production DB, restore from backup
  before retrying.

After remediation:

```
# still on the DB copy:
python manage.py migrate contacts 0004_party_data_model --fake       # unwind verify + backfill
python manage.py migrate contacts zero --fake                         # only if doing a full reset
# or simpler — drop /tmp/test.sqlite3, re-copy from production, repeat:
cp /path/to/production.sqlite3 /tmp/test.sqlite3
python manage.py migrate contacts 0005_backfill_party
python manage.py contacts_backfill_reconcile
```

Only deploy v2.0.0 to production once `contacts_backfill_reconcile`
exits green on a fresh copy.

### Why we gate the destructive migrations on this check

After step 4 the legacy `crm_contact` / `crm_customer` / `crm_supplier`
/ `crm_person` / `crm_customergroup` tables and the legacy FK columns
on documents and prices are **gone**. If the backfill missed a row and
we drop the source table, that row's data is irrecoverable from the
running application — restoring from a backup is the only option. The
verify migration makes that scenario loud-and-fast instead of
silent-and-late: if the counts don't match, the destructive migrations
never run.

## Things to be aware of

- **Do not `amend` or squash the split migrations after release.**
  Once `settings.0001_initial` is recorded in a production
  `django_migrations` table, renaming or splitting it further will
  re-introduce the "applied before its dependency" class of errors. Add
  *new* migrations instead.

- **`sync_split_migrations` only records migrations whose tables fully
  exist.** If you ship a migration that only adds columns (no
  `CreateModel`), that migration will *not* be auto-recorded and must
  run normally. That's usually what you want; the unusual case is
  dropping/renaming operations applied manually on a production DB,
  where you'll have to mark the migration applied by hand.

- **The SQLite `id` rebuild is bounded by a regex.** It matches
  `id integer NOT NULL` (without `PRIMARY KEY`). Tables declared with
  any other legacy id shape — e.g. a composite key, or
  `rowid integer primary key` with a surrogate `id` — won't be
  rewritten automatically. Inspect `_needs_id_upgrade` /
  `_rebuild_sqlite_table` and extend if you hit such a case.

- **PostgreSQL deployments take only step 3.** Step 1 (Django <1.9
  `django_migrations` schema) and step 2 (SQLite id rebuild) don't
  apply. The command guards each step with the appropriate vendor /
  schema check, so it's safe to run everywhere.

- **Fresh installs are unaffected.** On an empty database,
  `sync_split_migrations` finds no tables to reconcile, records
  nothing, and `migrate` runs the full graph from scratch.

## Where the pieces live

| Concern | Path |
|---|---|
| New core app | `koalixcrm/core/` |
| Core migrations | `koalixcrm/core/migrations/0001_initial.py`, `0002_transforms.py`, `0003_pdf_export_process_links.py`, `0004_pdf_export_process.py` |
| New contacts app | `koalixcrm/contacts/` |
| Contacts migrations | `koalixcrm/contacts/migrations/0001_initial.py`, `0002_initial.py`, `0003_add_postaladdress_subdivision_code.py` |
| Idempotent migration ops | `koalixcrm/migration_utils.py` |
| Reconciliation command | `koalixcrm/core/management/commands/sync_split_migrations.py` |
| REST façade (core) | `koalixcrm/core_api_py/` |
| REST façade (contacts) | `koalixcrm/contacts_api_py/` |
| REST façade (trimmed) | `koalixcrm/products_api_py/` |
| URL wiring | `projectsettings/urls.py` |
| Entrypoint wiring | `docker/dev/entrypoint.sh`, `docker/prod/entrypoint.sh` |
| Reference test DBs | `/app/koalixcrm_data/db/auftraegekoalixnet_20230101.sqlite3`, `/app/koalixcrm_data/db/olddb.sqlite3` |
