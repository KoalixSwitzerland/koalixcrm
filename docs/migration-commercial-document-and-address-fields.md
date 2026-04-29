# Migration guide: CommercialDocument & Address field changes

## Scope

This change touches two models in koalixcrm:

1. `contracts.CommercialDocument` (`crm_commercialdocument`)
2. `contacts.Address` (`crm_address`)

It is a **schema + data migration**, not just a rename. Read this whole
document before running migrations against a populated database.

## What changes

### CommercialDocument

| Old | New | Notes |
|---|---|---|
| `external_reference` (CharField, max_length=100) | `party_reference` (CharField, max_length=100) | pure rename — `RenameField` preserves data |
| — | `ext_business_appl_references` (JSONField, blank=True, default=dict) | new field. Holds external business-application references as a JSON object: `{"Bexio": "AU-9909", "Comatic": "AR-78786"}`. No backfill of existing rows is performed; existing rows get the model `default=dict` semantics (an empty `{}`) on read after the schema migration. |

The corresponding XSL templates under `koalixcrm/core/static/default_templates/{de,en}/`
read `field[@name='external_reference']` against the legacy `crm.salesdocument`
model name. These references are updated to `field[@name='party_reference']`
so that newly rendered PDFs continue to print the value.

> **Note on legacy model name.** The XSL still references
> `model='crm.salesdocument'` — this is a historical fixture name from before
> the v2.0.0 split and is unrelated to the field rename. We do not change
> the model name here; we only update the field name attribute.

### Address

The "single address line + line 2 + line 3" shape is replaced with a
structured street/number + two additional lines:

| Old | New | Notes |
|---|---|---|
| `address_line_1` (CharField, max_length=200) | `street` (CharField, max_length=200, blank=True, null=True) **and** `number` (CharField, max_length=16, blank=True, null=True) | **split** by data migration — see "Split rule" below |
| `address_line_2` (CharField, max_length=200) | `additional_address_line_1` (CharField, max_length=200, blank=True, null=True) | rename, data preserved |
| `address_line_3` (CharField, max_length=200) | `additional_address_line_2` (CharField, max_length=200, blank=True, null=True) | rename, data preserved |
| `address_line_4` (CharField, max_length=200) | `additional_address_line_3` (CharField, max_length=200, blank=True, null=True) | rename, data preserved |

`number` is a **string**, not an integer. House numbers in real-world data
include letters and ranges (`12a`, `12-14`, `Bis 7`).

## Split rule (language-conditional)

The split heuristic is conditional on the project's configured language
(`settings.LANGUAGE_CODE`):

- **Languages that put the number AFTER the street** (DE, CH, FR, IT, AT,
  NL, ES, PT, …): the rule is **trailing token starting with a digit**.
  - Example: `"Musterstraße 12a"` → `street="Musterstraße"`, `number="12a"`
  - Example: `"Bahnhofstrasse 1"` → `street="Bahnhofstrasse"`, `number="1"`
- **Languages that put the number BEFORE the street** (EN-US, EN-GB, EN-CA,
  …): the rule is **leading token starting with a digit**.
  - Example: `"123 Main St"` → `number="123"`, `street="Main St"`
  - Example: `"742 Evergreen Terrace"` → `number="742"`, `street="Evergreen Terrace"`

The data migration reads `django.conf.settings.LANGUAGE_CODE` once at
migration time. If the configured language is one of the explicit "leading
number" locales (`en`, `en-us`, `en-gb`, `en-ca`, `en-au`), the leading-token
rule is used. Otherwise the trailing-token rule is used (European default,
matching the historical koalixcrm customer base).

### Fallback

If the address line does not match the active rule (e.g. "PO Box 1234",
"Postfach 1234", or any unparseable string), the **whole** `address_line_1`
goes into `street` and `number` is left empty (`""`/`NULL`). No data is
discarded.

### Empty / NULL inputs

`address_line_1 = NULL` or `""` → `street = NULL`, `number = NULL`.

## Migration plan

The migrations follow the standard Django three-step pattern for non-destructive
data moves: **add new fields → data-migrate → remove old fields**. Splitting
across multiple migration files keeps each step reviewable and lets a deploy
roll back to an intermediate state if needed.

### `contracts/migrations/00XX_commercialdocument_field_renames.py`

1. `RenameField('CommercialDocument', 'external_reference', 'party_reference')`
2. `AddField('CommercialDocument', 'ext_business_appl_references',
   JSONField(blank=True, default=dict))`

No data migration required. Existing rows automatically read `{}` for the new
JSON field (Django applies the default at read time for NULL values; for
`JSONField` the column is NOT NULL by default with `default=dict`).

### `contacts/migrations/00XX_address_split_step1_add.py`

`AddField` for `street`, `number`, `additional_address_line_1`,
`additional_address_line_2`, `additional_address_line_3` — all five added
as nullable so the migration can run on a populated table without a default
backfill in DDL.

### `contacts/migrations/00XX_address_split_step2_data.py`

`RunPython` data migration that, for every `Address` row:

1. Copies `address_line_2` → `additional_address_line_1`.
2. Copies `address_line_3` → `additional_address_line_2`.
3. Copies `address_line_4` → `additional_address_line_3`.
4. Splits `address_line_1` into `(street, number)` using the language-conditional
   rule above.

The data migration MUST use the historical model accessed via
`apps.get_model('contacts', 'Address')` so it remains correct if model code
changes later. It MUST NOT import the live model class.

A reverse function joins `street + " " + number` back into `address_line_1`
(and copies the additional lines back) so the migration is reversible for
test purposes.

### `contacts/migrations/00XX_address_split_step3_remove.py`

`RemoveField` for `address_line_1`, `address_line_2`, `address_line_3`, `address_line_4`.

> **Why three files, not one.** A single migration mixing schema and data
> can be hard to roll back partially. Splitting lets you stop at step 2 in
> production, verify the split looks correct in a sample of rows, and only
> then run step 3 (which is the destructive one).

## Call sites updated alongside the model change

- `koalixcrm/contracts/admin/commercial_document_admin.py` — `external_reference`
  in `fieldsets` becomes `party_reference`; `ext_business_appl_references`
  added as a read-only JSON textarea (admins edit Bexio/Comatic refs by
  hand for now — no guided editor in scope).
- `koalixcrm/contacts/admin/party_admin.py` — `list_display` and
  `search_fields` referencing `address_line_1` switch to `street`. (Searching
  by house number alone is rarely useful; `street` is the primary index.)
- `koalixcrm/contacts/serializers/party_serializers.py` — replace the three
  `address_line_*` field names with `street`, `number`,
  `additional_address_line_1`, `additional_address_line_2`,
  `additional_address_line_3`.
- `koalixcrm/contracts/serializers/nested_commercial_document.py` — the
  `SerializerMethodField` accessors for `address_line_1/2/3` are replaced
  with accessors for `street`, `number`, `additional_address_line_1`,
  `additional_address_line_2`. The `Meta.fields` tuple is updated.
  `external_reference` in the same `Meta.fields` becomes `party_reference`,
  and `ext_business_appl_references` is added.
- `koalixcrm/djangoUserExtension/serializers/user_extension_nested.py` —
  same field-name updates against the `address.*` source paths.
- `koalixcrm/contacts_api_py/dto/party_dtos.py` — DTO attribute names
  follow the model. Outbound mappers (e.g. to Bexio) that previously emitted
  `address_line_1` must now build that field from `street + " " + number`.
- `koalixcrm/contracts_api_py/dto/{commercial_document,quotation,invoice,
  credit_note,sales_order,purchase_order,despatch_advice,payment_reminder}.py` —
  DTO attribute `external_reference` → `party_reference`; new attribute
  `ext_business_appl_references` (defaulting to `{}`).
- `koalixcrm/contacts/backfill.py` — both the `csv_row` reader and the
  `PostalAddress`-creation block use the old field names. The migration
  has not yet been run on the legacy CSV columns, so the **CSV side keeps
  the old column names** (the legacy file format does not change), but the
  ORM write is updated to `street`/`number`/`additional_address_line_*`,
  splitting at write-time using the same rule.
- `koalixcrm/contracts/migrations/0013_*.py`,
  `koalixcrm/contracts/migrations/0014_*.py`,
  `koalixcrm/djangoUserExtension/migrations/0005_*.py`,
  `koalixcrm/contacts/migrations/0004_party_data_model.py` — these are
  **historical migrations** and are not modified. They use the field names
  that existed at the time they were written, accessed via
  `apps.get_model(...)`. The new migration files come after them and only
  affect the current schema.
- `koalixcrm/core/management/commands/koalixcrm_install_defaulttemplates.py` —
  the seed `address_line_1="Ave 1"` becomes `street="Ave"`, `number="1"`
  (the seeded value is in EN, so the leading-number rule applies).
- `koalixcrm/core/static/default_templates/{de,en}/{invoice,quotation,
  salesorder,purchaseorder,despatchadvice}.xsl` — every
  `field[@name='address_line_1']` is replaced with a concatenation of
  `field[@name='street']` and `field[@name='number']` (XSL `concat(...)`
  with a separator space). `address_line_2`, `address_line_3`,
  `address_line_4` become `additional_address_line_1`,
  `additional_address_line_2`, `additional_address_line_3` respectively.
  `field[@name='external_reference']` becomes `field[@name='party_reference']`.
- `tests/contacts/test_party_models.py`, `tests/contacts/test_convert_party_type.py`,
  `tests/factories/contacts/postal_address_factory.py`,
  `tests/factories/contracts/commercial_document_factory.py` — update test
  data to the new field names. The factory keeps `"Main-street 5"` as the
  default seed but split into `street="Main-street"`, `number="5"`.

## Acceptance criteria (for manual testing)

1. `python manage.py migrate` runs cleanly on a fresh database.
2. `python manage.py migrate` runs cleanly on a database populated by
   v1.14.0 fixtures, and afterwards a sample of 5+ addresses shows the
   street/number split correctly under the configured `LANGUAGE_CODE`.
3. `python manage.py check` reports no system errors.
4. The Django admin pages for `Address`, `Party`, and `CommercialDocument`
   render and the new fields are editable.
5. Generating an Invoice / Quotation / SalesOrder / PurchaseOrder /
   DespatchAdvice PDF using both the DE and EN default templates produces
   output where the address line shows `"<street> <number>"` and the
   document still shows the old "external reference" value (now under
   `party_reference`).
6. The party serializer JSON output contains `street`, `number`,
   `additional_address_line_1`, `additional_address_line_2`,
   `additional_address_line_3` and no longer contains `address_line_1/2/3/4`.
7. The commercial-document serializer JSON output contains
   `party_reference` and `ext_business_appl_references` and no longer
   contains `external_reference`.

## Out of scope

- Backfilling `ext_business_appl_references` for existing CommercialDocument
  rows. They start as `{}` and are populated by hand or by future sync code.
- A guided UI for editing `ext_business_appl_references` — Django admin
  raw JSON textarea is sufficient for now.
- Changing the legacy CSV format consumed by `contacts/backfill.py`.
- The v1.x `crm.postaladdress` legacy fixture / model name in the XSL
  selectors — the XSL keeps `object[@model='crm.postaladdress']` as a
  historical name but updates the inner `field[@name='...']` selectors.
