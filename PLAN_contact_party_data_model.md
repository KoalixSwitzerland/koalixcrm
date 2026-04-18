# Plan: Contact / Party Data Model (issue #198)

**Status:** accepted — to be executed as four sequential issues / four PRs
**Release:** ships with **v2.0.0** (major version break, no backwards-compat promise)
**Target apps:** `koalixcrm.contacts` (primary), `koalixcrm.contracts`, `koalixcrm.products`, `koalixcrm.reporting`, `koalixcrm.djangoUserExtension`, `koalixcrm.contacts_api_py`, `app_api_java`
**Authoritative ADR:** [`koalixcrm_system/adr/0001-contact-and-party-data-model.md`](../koalixcrm_system/adr/0001-contact-and-party-data-model.md)
**GitHub issue:** [KoalixSwitzerland/koalixcrm#198](https://github.com/KoalixSwitzerland/koalixcrm/issues/198)
**Deciders:** @scaphilo, @Hacont — *"standardize wherever possible"* → UBL 2.3 vocabulary is authoritative.

> **v2.0.0 clean-break decision (2026-04-17, @scaphilo + @Hacont):**
>
> Since this ships with the v1.14.0 → v2.0.0 major version bump, we explicitly trade API
> backwards-compatibility for a simpler migration. That changes the shape of PR #3 and PR #4
> materially — summarised in [§ v2.0.0 clean-break simplifications](#v200-clean-break-simplifications)
> below, with the per-PR sections updated in place. **Data migration is preserved** (the legacy
> rows still get migrated into the new Party tables) — the break is on API surface only:
>
> - no deprecation headers, no `Deprecation:` / `Sunset:` HTTP shims, no read-only legacy routes,
> - no "keep the old FK as a nullable shadow for one release",
> - no transitional dual-admin / dual-serializer / dual-viewset layers kept around,
> - no staged tightening of NOT NULL constraints across two PRs.
>
> Everything already committed on `issue/392-…`, `issue/393-…`, and `issue/394-…` stays useful —
> the simplification collapses the *remaining* work into the expanded PR #4 described below.

---

## Context

Issue #198 (open since 2018) asks to split our contact management into:

- **Contact** = private person
- **Organization** = legal person (AG, GmbH, Verein, Holding, …)
- **Link Contact ↔ Organization** with hierarchical position
- **Link Organization ↔ Organization**
- **Addresses linked, not hard-referenced**

The ADR accepts the direction *and* aligns naming with **UBL 2.3** (already binding for
`CommercialDocument` — see `PLAN_commercial_document_ubl_alignment.md`, which explicitly defers
this "Party abstraction" work to a separate RFC; the ADR fills that slot).

### Current state (today's reality in `koalixcrm/contacts/models/`)

- `Contact` — base of MTI hierarchy, semantically organization-like.
- `Customer(Contact)`, `Supplier(Contact)` — MTI subclasses.
- `Person` — natural person with duplicate `email`/`phone` fields, M2M to `Contact` via
  `ContactPersonAssociation`.
- `PostalAddressForContact` / `EmailAddressForContact` / `PhoneAddressForContact` — concrete
  inheritance, hard FK to `Contact` (field confusingly named `person`).
- External FKs that pin the current naming:
  - `contracts.Contract.default_customer → contacts.Customer`
  - `contracts.CommercialDocument.customer → contacts.Customer`
  - `products.Price`, `products.CustomerGroupTransform` → `contacts.CustomerGroup`
- Ripple surfaces: **37 files** import from `koalixcrm.contacts`; Python DTO mirror
  (`koalixcrm/contacts_api_py/`) and Java DTO mirror (`app_api_java/.../ContactDto.java`) also need
  to move.

### Target state (per ADR §3)

```
Party (concrete, FK target for documents)
 ├── Organization(Party)       — MTI; legal form, reg nr, VAT/UID via PartyIdentification
 └── Contact(Party)            — MTI; natural person, GDPR fields

PartyRole              — replaces Customer/Supplier subclasses (customer|supplier|lead|…)
PartyIdentification    — VAT/UID/GLN/DUNS/LEI/internal, per-scheme, with validity
OrganizationMembership — Contact × Organization (title, position, is_primary, validity)
OrganizationRelationship — Organization × Organization (parent_of|partner_of|…, validity)
Address / AddressAssignment        — loose link, purpose + validity
PhoneNumber / PhoneAssignment      — loose link, purpose + validity
EmailAddress / EmailAssignment     — loose link, purpose + validity
PartyGroup / PartyGroupMembership  — replaces CustomerGroup, with role_type_scope
```

---

## Why four PRs

Mechanical but pervasive; one PR would be unreviewable. Split gives clean bisect, independent
review, and — critically — lets us pause between phases if priorities shift without leaving the
repo in a half-migrated state.

| PR | Title | Touches | DB migrations | Risk |
|---|---|---|---|---|
| #1 (#392) | Additive schema (new Party / Organization / Contact / … tables) | `contacts/` only | 1 schema migration (additive) | Low |
| #2 (#393) | Data migration into new tables | `contacts/` only | 1 data migration (`RunPython`) | **High** — production data |
| #3 (#394) | **Add** new FKs alongside legacy + new admin / DRF / DTOs | `contracts/`, `products/`, `contacts_api_py/`, `app_api_java/` | 1 FK-add migration per app | Medium — hot path (invoicing) |
| #4 (#395) | **Drop** legacy models, FKs, admin, DRF, DTOs, REST routes + rename transitional classes + PDF worker alignment | `contacts/`, `contracts/`, `products/`, `reporting/`, `djangoUserExtension/`, `contacts_api_py/`, `app_api_java/`, `pdf-export-service/` | 1 destructive migration per app | Medium — large surface but mechanical |

Each PR remains shippable in isolation in the sense that the codebase compiles and tests pass.
The v2.0.0 release is cut **after #4 merges** — between #3 and #4 the API carries both legacy and
new shapes, but that window is internal to the release train; external consumers only see the
post-#4 API.

### v2.0.0 clean-break simplifications

The per-PR sections below were drafted before the v2.0.0 clean-break decision and still contain
transitional-era language in places. The following **overrides** apply — take them as the source
of truth where they conflict with the older wording:

- **PR #3 (#394).** *Already committed as phases A–F.* No further work needed in this PR.
  Phase G (REST deprecation shims on `/api/customers/` etc.) and Phase H (soft-warning
  `CommercialDocument.clean()` validation) are **cancelled** — they were coexistence-era
  polish. Their intent is absorbed into #4: legacy routes get deleted outright, and the
  `party`-has-active-`customer`-role rule goes straight to a hard constraint alongside the
  NOT NULL migration.
- **PR #4 (#395) expanded scope** (see [§ PR #4](#pr-4--drop-legacy-models--code)):
  1. Drop legacy models (`Contact`, `Customer`, `Supplier`, `Person`, `CustomerGroup`, all
     `*ForContact` satellites) and their DB tables.
  2. Drop legacy FK *columns* on documents (`Contract.default_customer`, `Contract.default_supplier`,
     `CommercialDocument.customer`, `Price.customer_group`,
     `CustomerGroupTransform.from_/to_customer_group`).
  3. Tighten the new FKs to `NOT NULL` in the same migration.
  4. Delete legacy admin, DRF serializers, viewsets, REST routes, Python DTOs, Java DTOs.
     **No deprecation shim, no read-only legacy route, no deprecated-alias class.**
  5. Rename transitional classes and files: `PartyContact` → `Contact`, `PartyEmail` →
     `EmailAddress` (Django class + db_table + .py file + Java DTO + Python DTO + serializer +
     viewset + every import site).
  6. Restructure `djangoUserExtension` satellite models (`UserExtensionPostalAddress` /
     `-PhoneAddress` / `-EmailAddress`) — they can no longer inherit from the legacy base
     classes (the bases are being deleted). Either flatten to standalone models or rebuild on
     the new `Address` / `PhoneNumber` / `PartyEmail` types with a user-specific assignment
     table. Decision to be taken in the PR.
  7. Update `nested_commercial_document.py` (Python) and the Java `ContactDto` record together
     to emit and consume Party-shaped JSON. PDF worker XSL-FO templates change in the same PR.
  8. Add the **hard** validation: `Contract.buyer_party` / `CommercialDocument.party` must have
     an active `PartyRole(role_type='customer')` at the document's `issue_date`. Enforced in
     `clean()` + serializer + admin; no "warning only" phase.

---

## PR #1 — Additive schema

### Goal

Add the new Party data model **without removing or renaming anything**. Old and new models coexist.
No external FKs change in this PR.

### Scope — new models in `koalixcrm.contacts.models`

| New model | File | Notes |
|---|---|---|
| `Party` | `party.py` | Concrete Django model; `id` BigAutoField, `display_name`, audit fields |
| `Organization` | `organization.py` | `OneToOneField(Party, primary_key=True)` (MTI) + `legal_form`, `legal_name`, `registration_number`, `legal_seat_country` |
| `Contact` *(new)* | `natural_person.py` — tentative filename to avoid colliding with legacy `contact.py` during PR #1 | MTI; `prefix`, `given_name`, `family_name`, `date_of_birth`, `gdpr_consent_date`, `preferred_language` |
| `PartyIdentification` | `party_identification.py` | `party`, `scheme` (VAT/UID/GLN/…), `value`, `valid_from/to` |
| `PartyRole` | `party_role.py` | `party`, `role_type` (customer/supplier/lead/…), `valid_from/to`, `is_primary` |
| `OrganizationMembership` | `organization_membership.py` | `contact`, `organization`, `title`, `position`, `is_primary`, `valid_from/to` |
| `OrganizationRelationship` | `organization_relationship.py` | `parent`, `child`, `relationship_type`, `valid_from/to` |
| `Address` | `address.py` | Standalone — same fields as today's `PostalAddress` |
| `AddressAssignment` | `address_assignment.py` | `party`, `address`, `purpose`, `is_primary`, `valid_from/to` |
| `PhoneNumber` | `phone_number.py` | `phone_e164` |
| `PhoneAssignment` | `phone_assignment.py` | `party`, `phone`, `purpose`, … |
| `EmailAddress` *(new)* | `email_mailbox.py` — tentative filename to avoid colliding with legacy `email_address.py` | `email` |
| `EmailAssignment` | `email_assignment.py` | `party`, `email`, `purpose`, … |
| `PartyGroup` | `party_group.py` | `name`, `role_type_scope` (nullable) |
| `PartyGroupMembership` | `party_group_membership.py` | `party`, `party_group` |

> **Naming collision note:** the legacy `contact.py` defines class `Contact`, and the new
> `Contact(Party)` has the same class name but opposite semantics. During PR #1 the new class
> lives in a differently-named module (`natural_person.py`) and is imported under an explicit
> alias in `contacts/models/__init__.py`:
>
> ```python
> from koalixcrm.contacts.models.natural_person import Contact as PartyContact  # transitional
> ```
>
> The rename to the canonical `contact.py` happens in **PR #4** after the legacy class is dropped.

### Scope — admin & API (read-only scaffolding)

- Minimal `ModelAdmin` for each new model — just registration + list display, no inlines yet.
  Full admin UX arrives in PR #3 when the models are actually authoritative.
- **No DRF viewsets / serializers** in PR #1. (Avoids API-shape debate while schema is still being
  validated.)
- No factory_boy factories yet — added alongside PR #2 so they exercise the data migration.

### Scope — migration

- **Single migration** `contacts/migrations/0004_party_data_model.py`, purely additive:
  `CreateModel` for all 15 new models, in dependency order (Party first, then MTI subclasses, then
  side tables, then assignments, then groups).
- No `RunPython`. No FK changes on existing models.
- `python manage.py migrate` must succeed on a fresh DB and on a production-snapshot DB.

### Acceptance criteria

- `python manage.py makemigrations --check --dry-run` is clean.
- `python manage.py migrate` runs clean on fresh DB.
- `python manage.py migrate` runs clean on a DB that has `0003_add_postaladdress_subdivision_code`
  applied (= current head).
- Model-level pytest suite covers every new model: can create, can save, can `__str__`.
- No change to any REST endpoint, admin URL, or externally-observable behaviour.
- Changelog entry: *"New Party data model introduced alongside legacy Contact/Customer/Supplier.
  Not yet used by any document. See issue #198, PR #2 for data migration."*

### Out of scope for PR #1

- Any data migration (PR #2).
- Any FK change on `Contract`, `CommercialDocument`, `Price`, … (PR #3).
- Dropping legacy models (PR #4).
- Duplicate detection, merge UI, GDPR tooling.

---

## PR #2 — Data migration into new tables

### Goal

Populate the new Party tables from the existing `Contact`/`Customer`/`Supplier`/`Person` rows
and their address/phone/email satellites. After this PR, every piece of information in the legacy
tables has an equivalent representation in the new tables. **Legacy tables remain authoritative
for document FKs** — the swap happens in PR #3.

### Scope — data migration

Single Django migration `contacts/migrations/0005_backfill_party.py` with a `RunPython` forward
step and a reverse step that truncates the new tables (safe because PR #1's migration created them
empty). Migration logic:

1. **For each `contacts.Contact` row** (org-like in current semantics):
   - Create `Party(display_name=contact.name)`.
   - Create `Organization(party=…, legal_name=contact.name)`. `legal_form`, `registration_number`
     stay blank — best-effort enrichment is a separate tool, not a migration concern.
   - Stash mapping `legacy_contact_id → new_party_id` in a temporary dict (or a throwaway
     `LegacyContactMapping` table if the dataset is too large — rule of thumb: use table if
     `Contact.objects.count() > 100_000`).
2. **For each `contacts.Customer` row** (which is also a `Contact` via MTI):
   - Do **not** create a new Party — the parent `Contact` row already generated one in step 1.
   - Create `PartyRole(party=mapped, role_type='customer', is_primary=True, valid_from=epoch)`.
3. **For each `contacts.Supplier` row** (same MTI shape):
   - Same as 2 but `role_type='supplier'`.
4. **For each `contacts.Person` row**:
   - Create `Party(display_name=f"{prefix} {pre_name} {name}")`.
   - Create `Contact(party=…, prefix, given_name=pre_name, family_name=name,
     gdpr_consent_date=null)`.
   - Stash `legacy_person_id → new_party_id`.
   - If `person.email` is set → create `EmailAddress(email=…)` (dedup by exact match across the
     whole table) and `EmailAssignment(party=…, purpose='primary', is_primary=True)`.
   - Same for `person.phone` → `PhoneNumber` + `PhoneAssignment`.
5. **For each `contacts.ContactPersonAssociation` row** (M2M Person × Contact):
   - Create `OrganizationMembership(contact=mapped_person, organization=mapped_contact,
     title=legacy.person.role, is_primary=False, valid_from=epoch)`.
6. **For each `PostalAddressForContact` row**:
   - Build an `Address` row (dedup across the table by full tuple of address fields; first
     occurrence wins).
   - Create `AddressAssignment(party=mapped_contact, address=deduped_address,
     purpose=mapping(legacy.purpose), is_primary=False, valid_from=epoch)`.
7. **For each `EmailAddressForContact` row** → `EmailAddress` + `EmailAssignment`, dedup on exact
   email.
8. **For each `PhoneAddressForContact` row** → `PhoneNumber` + `PhoneAssignment`, dedup on exact
   phone.
9. **For each `CustomerGroup` row** → `PartyGroup(name=…, role_type_scope='customer')`.
10. **For each `Customer.is_member_of` M2M row** → `PartyGroupMembership(party=mapped, group=…)`.

### Scope — invariants that must hold after migration

These are implemented as assertions at the end of the `RunPython` forward function, **and** as
standalone integrity tests in `contacts/tests/test_backfill_invariants.py`:

- `Party.objects.count() == Contact.objects.count() + Person.objects.count()` (legacy).
- `Organization.objects.count() == Contact.objects.count()` (legacy, org-like).
- `PartyRole.objects.filter(role_type='customer').count() == Customer.objects.count()`.
- `PartyRole.objects.filter(role_type='supplier').count() == Supplier.objects.count()`.
- Every `PostalAddressForContact` row has exactly one matching `AddressAssignment` (by party +
  address field equality).
- `OrganizationMembership.objects.count() == ContactPersonAssociation.objects.count()`.

### Scope — dry-run & reconciliation

- Management command `manage.py contacts_backfill_dryrun` that prints the planned row counts per
  entity without writing anything. Run this on a production-sized snapshot **before** applying the
  real migration.
- Management command `manage.py contacts_backfill_reconcile` that re-checks the invariants above
  post-migration and prints diffs. Run in staging and on production immediately after deploy.

### Acceptance criteria

- Dry-run output on a production-sized snapshot matches expected totals (manual review by @scaphilo
  or @Hacont).
- Migration forward + reverse both complete cleanly on a DB that has PR #1 applied.
- All invariant tests green.
- Legacy tables are **unmodified** (read-only view into history for the duration of PR #3 / #4).
- Changelog entry: *"Legacy contact data backfilled into new Party tables. No document FKs changed
  yet — legacy tables remain authoritative."*

### Out of scope for PR #2

- Any change to `contracts.*` / `products.*` / external FKs (PR #3).
- Dropping any legacy table (PR #4).
- Merge / dedup beyond exact-match on postal address, email, phone (tracked separately).

---

## PR #3 — Rewire external FKs to `Party`

### Goal

Change every external reference to `contacts.Customer` / `contacts.Supplier` / `contacts.Contact` /
`contacts.Person` / `contacts.CustomerGroup` to target the new `Party` / `PartyGroup` model.
After this PR, `Party` is authoritative — the legacy models still exist but nothing outside the
`contacts` app references them.

### Scope — FK migrations (app by app)

| App / model | Old FK | New FK | Migration file |
|---|---|---|---|
| `contracts.Contract.default_customer` → `contacts.Customer` | **→** `buyer_party` → `contacts.Party` | `contracts/migrations/00XX_party_fk.py` |
| `contracts.CommercialDocument.customer` → `contacts.Customer` | **→** `party` → `contacts.Party` | same migration |
| `products.Price.customer_group` → `contacts.CustomerGroup` | **→** `party_group` → `contacts.PartyGroup` | `products/migrations/00XX_party_group_fk.py` |
| `products.CustomerGroupTransform.from_customer_group` / `.to_customer_group` | **→** `from_party_group` / `to_party_group` | same migration |
| `djangoUserExtension.UserExtension.*` | — no FK to `Customer` / `Supplier` / `Contact` / `Person` / `CustomerGroup` (verified 2026-04-17). Satellite models `UserExtensionPostalAddress` / `-PhoneAddress` / `-EmailAddress` inherit from legacy `PostalAddress` / `PhoneAddress` / `EmailAddress` (concrete-table inheritance) and must be restructured in PR #4 when those bases are dropped. | *(n/a — moved to PR #4)* |

For each FK swap migration:

1. Add the **new nullable** FK field alongside the old one.
2. `RunPython` step: populate new FK from old FK using the backfill mapping.
3. Do **not** drop the old FK field in PR #3 — keep it as a nullable shadow for one release for
   rollback safety. Removal in PR #4.

### Scope — admin / DRF / templates / DTO mirrors

Every file currently importing `Customer`, `Supplier`, `Contact` (legacy), `Person`, or
`CustomerGroup` from `koalixcrm.contacts.*` gets rewired. Inventory (known from current grep —
37 files, full list below):

- **Models** (8): `contracts/models/{contract.py,commercial_document.py,purchase_order.py}`,
  `products/models/{price.py,customer_group_transform.py}`,
  `contacts/models/{contact.py,customer.py,supplier.py}` *(legacy models — imports cleaned so
  nothing external references them)*.
- **Admin** (7): `contacts/admin/{customer_admin.py,supplier_admin.py,customer_group_admin.py,
  customer_billing_cycle_admin.py,person_admin.py,contact_inlines.py,call_admin.py}`.
  After PR #3 these register **the new** `Party` / `Organization` / `Contact` / `PartyRole` /
  `PartyGroup` admins; the legacy admin registrations are deleted in PR #4.
- **Serializers** (6): `contacts/serializers/{contact_serializer.py,customer_serializer.py,
  supplier_serializer.py,person_serializer.py,customer_group_serializer.py,
  customer_billing_cycle_serializer.py}` → new serializers mirroring new models.
- **Views / DRF viewsets** (9): `contacts/views/{contact_view_set.py,customer_view_set.py,
  supplier_view_set.py,person_view_set.py,customer_group_view_set.py,customer_billing_cycle_view_set.py,
  contact_email_address_view_set.py,contact_phone_address_view_set.py,contact_postal_address_view_set.py}`.
- **Python API mirror** (4): `contacts_api_py/{__init__.py,contacts_api.py,contacts_api_client.py,
  dto/__init__.py}` — add `PartyDto`, `OrganizationDto`, `ContactDto` (new shape),
  `PartyRoleDto`, `AddressDto`, `AddressAssignmentDto`, …
- **Cross-app imports** (3): `reporting/serializers/resource_price_serializer.py`,
  `djangoUserExtension/models/user_extension.py`, `contracts/serializers/nested_commercial_document.py`.
- **Java DTO mirror** (`app_api_java/src/main/java/net/koalix/api/dto/`): add `PartyDto.java`,
  `OrganizationDto.java`, rewrite `ContactDto.java` for the new semantics (class renamed with
  deprecated alias for one release).

### Scope — REST API strategy

- **New resources:** `/api/parties/`, `/api/organizations/`, `/api/contacts/` *(new semantics: natural
  persons)*, `/api/party-roles/`, `/api/addresses/`, `/api/party-groups/`.
- **Legacy resources kept for one deprecation release** with `Deprecation:` and `Sunset:` headers:
  - `/api/customers/` → read-only view over `Party` filtered by `role='customer'`.
  - `/api/suppliers/` → read-only view over `Party` filtered by `role='supplier'`.
  - `/api/persons/` → read-only view over new `Contact` resource.
  - `/api/customer-groups/` → read-only view over `PartyGroup` filtered by
    `role_type_scope='customer'`.
  - **Removed in PR #4.**

### Scope — validation rule

Domain invariant (admin validation + serializer validation + `CommercialDocument.clean()`):

> A `Contract.buyer_party` / `CommercialDocument.party` must have an active `PartyRole` with
> `role_type='customer'` at the document's `issue_date` (or `datetime.now()` for drafts).

Keep it a soft rule for now (warning + admin list filter) until we confirm no legacy data violates
it — promote to a hard constraint in a follow-up.

### Acceptance criteria

- All FK migrations apply cleanly on a DB that has PRs #1 + #2 applied.
- Full pytest suite passes.
- Manual smoke test: create a new quotation via admin end-to-end using a `Party` with a customer
  role; verify PDF generation.
- Deprecation headers present on legacy REST routes.
- Changelog entry lists new endpoints + legacy deprecation schedule.

### Out of scope for PR #3

- Dropping legacy models / tables / admin / serializers / viewsets (PR #4).
- Duplicate detection and merge UI.
- GDPR erasure tooling (separate issue after PR #4).

### Phase C verification findings (2026-04-17)

- **`djangoUserExtension.UserExtension`** has no FK to any legacy contacts model. Its three
  satellite classes (`UserExtensionPostalAddress` / `-PhoneAddress` / `-EmailAddress`) inherit
  from the legacy `PostalAddress` / `PhoneAddress` / `-EmailAddress` base models via concrete-table
  inheritance — **not** FKs. This coupling is therefore deferred to PR #4, which must either
  restructure these satellite models to use explicit fields (no inheritance) or migrate them onto
  the new `Address` / `PhoneNumber` / `PartyEmail` types with a user-specific assignment model.
- **`reporting.ResourcePrice`** is an MTI subclass of `products.Price` and automatically inherits
  the new `party_group` FK added in Phase B. No separate reporting migration needed.
- **`reporting/serializers/resource_price_serializer.py`** and
  **`contracts/serializers/nested_commercial_document.py`** still reference the legacy field names
  (`customer_group` and `customer` respectively). Deferred further to the Java-DTO work window —
  they are tightly coupled to the Java PDF worker's input shape, and rewriting them requires
  co-ordinated changes on the Java side. See Phase F findings below.

### Phase F deferrals (2026-04-17)

Phase F added Java DTO records for all 15 new Party-pattern endpoints (`PartyDto`,
`OrganizationDto`, `PartyContactDto`, …). It did **not**:

- **Rewrite `ContactDto`** (the legacy "org-like entity with nested addresses" record that
  `CommercialDocumentDto` embeds). The PDF worker still consumes that exact shape via
  `/invoices/<id>/nested/` etc. Rewriting it in-place would break PDF generation. The rewrite is
  staged for the post-#395 clean-up PR once the legacy `Customer`/`Contact` models are gone and
  the nested serializer can emit Party-shaped JSON safely.
- **Update `nested_commercial_document.py` and `resource_price_serializer.py`** on the Python
  side. Same reason: these are the producer side of the Java-consumed JSON. They flip together
  with the Java PDF worker in the post-#395 PR.
- **Update the PDF worker's XSL-FO builders or the `CrmApiClient` Java class** to consume the
  new DTOs. The PDF worker keeps reading the legacy shape; the new Java DTOs exist only as a
  preparatory mirror until a consumer is built.

Net effect: the Java and Python sides both have **both** shapes available (legacy + new), and
the PDF pipeline continues to use the legacy shape end-to-end until PR #395.

---

## PR #4 — Drop legacy models & code (v2.0.0 clean-break cutover)

### Goal

Single big cleanup PR that takes the repo from the dual-shape state left by PR #3 to the
post-v2.0.0 steady state where only the Party data model remains. No deprecation window, no
shims, no alias classes — this is the breaking change that the v1.14.0 → v2.0.0 bump licenses.

### Scope — destructive migrations

Per app, a single migration that (a) tightens new FKs to NOT NULL, (b) drops the legacy FK
columns, and (c) drops the legacy tables where applicable. All in the same migration so there's
no intermediate state where a document has neither a legacy customer nor a valid party.

- **`contacts/migrations/0006_drop_legacy_models.py`:**
  - `DeleteModel` for `Contact`, `Customer`, `Supplier`, `Person`, `ContactPersonAssociation`,
    `PostalAddressForContact`, `EmailAddressForContact`, `PhoneAddressForContact`,
    `CustomerGroup`.
  - Drops tables `crm_contact`, `crm_customer`, `crm_supplier`, `crm_person`,
    `crm_contactpersonassociation`, `crm_postaladdressforcontact`, `crm_emailaddressforcontact`,
    `crm_phoneaddressforcontact`, `crm_customergroup`.
  - Also the MTI-parent tables that inherit from `PostalAddress` / `PhoneAddress` /
    `EmailAddress` (the legacy base classes) need to be handled — see djUE restructure below.
  - Renames `crm_partycontact` → `crm_contact` and `crm_partyemail` → `crm_emailaddress`
    via `AlterModelTable`. (This is the v2.0.0 moment where the new table finally owns the
    canonical name.)
- **`contracts/migrations/0009_drop_legacy_customer_fks.py`:**
  - `AlterField` on `Contract.buyer_party` / `Contract.supplier_party` /
    `CommercialDocument.party` → `null=False, blank=False`.
  - `RemoveField` for `Contract.default_customer`, `Contract.default_supplier`,
    `CommercialDocument.customer`.
  - Precondition: a `RunPython` step asserts `Contract.objects.filter(buyer_party__isnull=True)`
    is empty and that every `CommercialDocument.party` is populated. Migration refuses to
    proceed otherwise.
- **`products/migrations/0003_drop_legacy_customer_group_fks.py`:**
  - `RemoveField` for `Price.customer_group`, `CustomerGroupTransform.from_customer_group`,
    `CustomerGroupTransform.to_customer_group`.
  - `AlterField` tightening `from_party_group` / `to_party_group` to `null=False`.
- **`djangoUserExtension/migrations/00XX_user_extension_satellite_restructure.py`:**
  - Restructures `UserExtensionPostalAddress` / `-PhoneAddress` / `-EmailAddress` — they can no
    longer inherit from the now-deleted legacy base classes. Default choice: flatten to
    standalone models with explicit fields (all the columns they need already live on the
    legacy-base rows and can be copied). Alternative (reuse new `Address` / `PhoneNumber` /
    `PartyEmail` + a `UserAddressAssignment`-style table) is cleaner but costs another PR
    after v2.0.0.

### Scope — code removal

**Delete outright:**

- Legacy model files: `koalixcrm/contacts/models/{customer.py, supplier.py, person.py,
  customer_group.py, postal_address.py, email_address.py, phone_address.py}`. (The legacy
  `contact.py` is replaced in-place — see rename below.)
- Legacy admin: `koalixcrm/contacts/admin/{customer_admin.py, supplier_admin.py, person_admin.py,
  customer_group_admin.py, call_admin.py, contact_inlines.py}`. (Keep
  `customer_billing_cycle_admin.py` — CustomerBillingCycle is retained.)
- Legacy DRF serializers: `koalixcrm/contacts/serializers/{customer_serializer.py,
  supplier_serializer.py, person_serializer.py, customer_group_serializer.py,
  contact_serializer.py}`.
- Legacy DRF viewsets: `koalixcrm/contacts/views/{customer_view_set.py, supplier_view_set.py,
  person_view_set.py, customer_group_view_set.py, contact_view_set.py,
  contact_postal_address_view_set.py, contact_phone_address_view_set.py,
  contact_email_address_view_set.py}`.
- Legacy REST routes: `/api/customers/`, `/api/suppliers/`, `/api/persons/`,
  `/api/customer_groups/`, `/api/contacts/`, `/api/contact_postal_addresses/`,
  `/api/contact_phone_numbers/`, `/api/contact_email_addresses/` — removed from
  `projectsettings/urls.py`. No read-only shims.
- Legacy Python DTOs: `koalixcrm/contacts_api_py/dto/{contact.py, customer.py, supplier.py,
  person.py, customer_group.py, postal_address.py, email_address.py, phone_address.py}` and
  the matching get / list / create / update methods on `KoalixCRMContactsAPIClient`.
- Legacy Java DTOs: `app_api_java/.../dto/{ContactDto.java, PostalAddressDto.java,
  EmailAddressDto.java, PhoneAddressDto.java}`.
- Any remaining `contacts.Customer` / `contacts.Supplier` / `contacts.Person` /
  `contacts.CustomerGroup` import anywhere in the tree — zero hits allowed after this PR.

**Rename the transitional classes to their canonical names (one operation per class, touching
Django model + admin + serializer + viewset + Python DTO + Java DTO + every import site):**

- `koalixcrm.contacts.models.natural_person.PartyContact` → `contact.Contact`.
  Rename class, rename `.py` file, `AlterModelTable('partycontact', 'contact')`, update
  `__init__.py` and every importer.
- `koalixcrm.contacts.models.party_email.PartyEmail` → `email_address.EmailAddress`.
  Same treatment.
- Python DTO `PartyContact` → `Contact`; Python DTO `PartyEmail` → `EmailAddress`.
- Java DTO `PartyContactDto` → `ContactDto` (replaces the legacy `ContactDto` that was deleted
  above); `PartyEmailDto` → `EmailAddressDto` (likewise).
- REST routes `/api/party_contacts/` → `/api/contacts/`; `/api/party_emails/` → `/api/emails/`
  (or drop `party_` prefix systematically from other routes if consistency is desired —
  decision TBD in the PR).

### Scope — cross-app serializer cutover

Items deliberately deferred from PR #3 Phase F:

- **`contracts/serializers/nested_commercial_document.py`** — replace `ContactNestedSerializer`
  with a `PartyNestedSerializer` that reads from the Party model. Field shape stays close to
  existing (the PDF worker's XSL-FO templates rely on it) but sources from `Party` +
  `AddressAssignment` + `EmailAssignment` + `PhoneAssignment` instead of the legacy satellites.
- **`reporting/serializers/resource_price_serializer.py`** — switch the `customer_group` field
  to `party_group` with the new serializer type. `ResourcePrice` already inherits `party_group`
  from `products.Price` via MTI; the field is present on the model.
- **`pdf-export-service/`** (Java PDF worker) — update the XSL-FO builders to consume the new
  JSON shape from the nested serializer. This is the *real* work on the Java side for v2.0.0
  and is the reason the legacy `ContactDto` could not be removed earlier.

### Scope — hard validation rule

Absorbed from the cancelled PR #3 Phase H (soft validation). Enforced at three levels in this PR:

- **Model:** `CommercialDocument.clean()` raises `ValidationError` if `self.party` has no
  active `PartyRole(role_type='customer')` at `self.issue_date`.
- **Serializer:** The new `CommercialDocumentSerializer` and subclasses re-check via
  `validate_party()`.
- **Admin:** `ModelAdmin.get_form` filters the `party` dropdown to parties with an active
  customer role.

Same rule for `Contract.buyer_party` (role=`customer`) and `Contract.supplier_party`
(role=`supplier`) at `Contract.start_date`. Hard constraint from day one — no warning-only
rollout.

### Scope — Python DTO cleanup

- Remove the 4 get / get_list / create / update methods each for `Customer`, `Supplier`,
  `Person`, `Contact` (legacy), `CustomerGroup`, and the 3 contact-address variants — 32
  methods total gone from `KoalixCRMContactsAPIClient`.
- After the class rename, drop the transitional `as PartyDto` / `as PartyContactDto` / etc.
  import aliases in `contacts_api_client.py`. The imports become plain `from … import Contact,
  Party, Organization, …`.

### Acceptance criteria

- Repo-wide grep for `contacts.Customer`, `contacts.Supplier`, legacy-semantics
  `contacts.Contact` (org-like), `contacts.Person`, `contacts.CustomerGroup`,
  `ContactPersonAssociation`, `PostalAddressForContact`, `EmailAddressForContact`,
  `PhoneAddressForContact` → **zero hits** outside migration history.
- Repo-wide grep for `PartyContact` / `PartyEmail` → zero hits (both renamed).
- `python manage.py migrate` applies cleanly and drops the legacy tables on both fresh DBs and
  DBs that have PR #3 applied.
- Full pytest suite passes, including end-to-end invoice PDF generation via the Java worker.
- CHANGELOG entry documents the breaking API changes:
  - Removed endpoints, removed DTOs, removed models, renamed types.
  - v2.0.0 release notes link to the UBL 2.3 `Party` mapping table for migration guidance.
- Git tag `v2.0.0` is cut **from this commit**.

### Out of scope for PR #4

- Squash of the four new migrations into one — follow-up housekeeping PR after v2.0.0 is in
  production.
- OpenAPI / REST API v2 schema overhaul — bigger topic, separate issue.
- Duplicate detection / merge UI, GDPR erasure tooling — tracked separately.

---

## GitHub issues — to be created (sub-tasks of #198)

1. **`#198.1`** — *Additive schema for Party data model* (PR #1). No dependencies.
2. **`#198.2`** — *Backfill migration from legacy contacts to Party* (PR #2). Blocked by #198.1.
3. **`#198.3`** — *Rewire document / product / report FKs to Party* (PR #3). Blocked by #198.2.
4. **`#198.4`** — *Drop legacy contact models and finalize naming* (PR #4). Blocked by #198.3.

Each sub-issue's body is the matching PR section above.

---

## Open questions (tracked here, resolved before PR #3)

1. `Party.display_name` — stored (maintained by signal) or derived? → **proposal: stored**;
   confirm with @scaphilo before PR #1 lands.
2. Internal customer number — belongs on `PartyIdentification` with `scheme='internal'`, or on a
   dedicated `Party.customer_number` field? → decide alongside PR #3.
3. Expose `PartyRole` via REST in v1 or admin-only? → decide alongside PR #3.
4. GDPR erasure policy on `Contact` — soft-delete + anonymize, or hard-delete with anonymized
   historical document copies? → verify CH OR art. 958f requirement with @scaphilo before the
   separate GDPR issue.
5. Minimum identification schemes at go-live — internal id + VAT/UID only, or also IBAN / LEI? →
   decide alongside PR #1.

---

## Timing

- PRs #1 and #2 can ship within a single release.
- PR #3 is the hot phase (invoicing impact). Ship it as its own release, with a data-migration
  dry-run on a production-sized snapshot first.
- PR #4 follows one release behind PR #3 (cosmetic cleanup; gives one rollback window).
