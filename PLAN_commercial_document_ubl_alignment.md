# Plan: `CommercialDocument` rename, `CreditNote`, and UBL 2.3 alignment

**Status:** proposal — to be split into two GitHub issues / two PRs
**Target app:** `koalixcrm.contracts`
**Timing:** execute **after** the monolith-split migration is fully applied — we want pure Django `RenameModel` / `AlterModelTable` operations on a stable baseline rather than rewriting `0001_initial` with `CreateModelIfNotExists` custom ops.

---

## Context

We recently split the koalixcrm monolith. The common base model for every sales-side document currently lives at `koalixcrm.contracts.models.sales_document.SalesDocument` (DB table `crm_salesdocument`) and is subclassed by `Invoice`, `Quote`, `PurchaseConfirmation`, `DeliveryNote`, `PaymentReminder`, `PurchaseOrder`.

Two motivations for this plan:

1. The name `SalesDocument` is inaccurate — purchase orders are not "sales" documents. `CommercialDocument` covers both directions.
2. We want to align document terminology with **UBL 2.3** so that future e-invoicing (Peppol, EN 16931, CH/EU mandates) maps cleanly onto our domain model without a translation layer.

## Why two PRs

Both changes are mechanical but pervasive. The scope of file touches:

- PR #1 (base rename + `CreditNote`): ~60 files, 2 migrations
- PR #2 (UBL subclass renames): ~30 more files, 1 migration per model renamed

Splitting gives: clean bisect, independent review, smaller merge-conflict surface with other work happening in `contracts/`, and the option to pause after PR #1 if priorities shift.

---

## PR #1 — Rename `SalesDocument` → `CommercialDocument` and add `CreditNote`

### Goal
Rename the shared base class (and its satellite models) to reflect that it covers both sales- and purchase-side commercial documents. Introduce a new `CreditNote` document type.

### Scope — rename

| Current | New |
|---|---|
| `SalesDocument` (model) | `CommercialDocument` |
| `SalesDocumentPosition` (model) | `CommercialDocumentPosition` |
| `TextParagraphInSalesDocument` | `TextParagraphInCommercialDocument` |
| `PostalAddressForSalesDocument` | `PostalAddressForCommercialDocument` |
| `EmailAddressForSalesDocument` | `EmailAddressForCommercialDocument` |
| `PhoneAddressForSalesDocument` | `PhoneAddressForCommercialDocument` |
| `SalesDocumentMedia` | `CommercialDocumentMedia` |
| `SalesDocument.derived_from_sales_document` | `CommercialDocument.derived_from_commercial_document` |
| DB table `crm_salesdocument` | `crm_commercialdocument` |
| DB table `crm_salesdocumentposition` (if present) | `crm_commercialdocumentposition` |
| DB table `crm_textparagraphinsalesdocument` | `crm_textparagraphincommercialdocument` |
| DB table `crm_postaladdressforsalesdocument` | `crm_postaladdressforcommercialdocument` |
| DB table `crm_emailaddressforsalesdocument` | `crm_emailaddressforcommercialdocument` |
| DB table `crm_phoneaddressforsalesdocument` | `crm_phoneaddressforcommercialdocument` |
| File `contracts/models/sales_document.py` | `contracts/models/commercial_document.py` |
| File `contracts/models/sales_document_position.py` | `contracts/models/commercial_document_position.py` |
| File `contracts/models/sales_document_media.py` | `contracts/models/commercial_document_media.py` |
| File `contracts/admin/sales_document_admin.py` | `contracts/admin/commercial_document_admin.py` |
| File `contracts/admin/sales_document_position_admin.py` | `contracts/admin/commercial_document_position_admin.py` |
| File `contracts/admin/sales_document_media_admin.py` | `contracts/admin/commercial_document_media_admin.py` |
| File `contracts/factory/sales_document_factory.py` | `contracts/factory/commercial_document_factory.py` |
| File `contracts/factory/sales_document_position_factory.py` | `contracts/factory/commercial_document_position_factory.py` |
| File `contracts/serializers/sales_document_serializer.py` | `contracts/serializers/commercial_document_serializer.py` |
| File `contracts/serializers/sales_document_position_serializer.py` | `contracts/serializers/commercial_document_position_serializer.py` |
| File `contracts/views/sales_document_position_view_set.py` | `contracts/views/commercial_document_position_view_set.py` |
| File `contracts_api_py/dto/sales_document.py` | `contracts_api_py/dto/commercial_document.py` |
| File `contracts_api_py/dto/sales_document_position.py` | `contracts_api_py/dto/commercial_document_position.py` |
| Class `OptionSalesDocument` | `OptionCommercialDocument` |
| Class `SalesDocumentInlinePosition` | `CommercialDocumentInlinePosition` |
| Class `SalesDocumentMediaInline` / `SalesDocumentMediaAdmin` | `CommercialDocumentMediaInline` / `CommercialDocumentMediaAdmin` |
| Class `SalesDocumentJSONSerializer` | `CommercialDocumentJSONSerializer` |
| Class `StandardSalesDocumentFactory` | `StandardCommercialDocumentFactory` |
| Variables / attribute names `sales_document` | `commercial_document` |

### Scope — new `CreditNote` model

- Sibling of `Invoice` under `CommercialDocument` (**not** a subclass of `Invoice`). UBL 2.3 treats `CreditNote` as its own root document type.
- Fields:
  - `corrects_invoice = ForeignKey(Invoice, on_delete=PROTECT, null=True, blank=True)` — optional pointer to the invoice being corrected (full credit, partial credit, or free-standing).
  - `status = CharField(choices=CREDITNOTESTATUS)` — mirror `Invoice.status` pattern (draft, issued, booked, cancelled).
  - `issue_date = DateField()` — document issue date.
  - `reason = CharField(max_length=200, blank=True)` — free-text reason for the credit note.
- Amount convention: positions store **positive** amounts on the credit note; the accounting booking reverses the sign. Do not store negative prices in `CommercialDocumentPosition`.
- Accounting: `register_credit_note_in_accounting(request)` — mirrors `Invoice.register_invoice_in_accounting` but reverses `from_account`/`to_account`.

### Scope — admin

- `CommercialDocumentAdmin` base (renamed from `OptionSalesDocument`).
- `CreditNoteAdmin(CommercialDocumentAdmin)` with:
  - `fieldsets += (("Credit Note specific", {"fields": ("corrects_invoice", "status", "issue_date", "reason")}),)`
  - Actions: `create_pdf_async`, `register_credit_note_in_accounting`, plus the usual document-conversion actions.
- `InlineCreditNote(admin.TabularInline)` — added to `OptionContract.inlines` so credit notes show on the contract detail page alongside quotes/invoices.
- **Admin actions — new:**
  - On `OptionContract`: `create_credit_note` — creates a blank credit note tied to the contract (no `corrects_invoice`).
  - On `OptionInvoice`: `create_credit_note_from_invoice` — creates a credit note pre-populated from the selected invoice, with `corrects_invoice` set and all positions copied with identical amounts.

### Scope — API

- New `CreditNoteJSONSerializer` in `contracts/serializers/credit_note_serializer.py`.
- New `CreditNoteViewSet` in `contracts/views/credit_note_view_set.py` — standard `ModelViewSet` with the usual permissions + filtering pattern.
- New DTO `contracts_api_py/dto/credit_note.py`.
- Wire `CreditNoteViewSet` into `contracts_api_py/contracts_api.py` `__all__` + URL router.
- Extend `contracts_api_client.py` to expose `credit_note` endpoints symmetric to `invoice`.

### Scope — factory

- `StandardCreditNoteFactory(StandardCommercialDocumentFactory)` in `contracts/factory/credit_note_factory.py`.
- Register in `contracts/factory/__init__.py`.

### Scope — tests

- API-level test cases (`tests/` or `koalixcrm/contracts/tests/`):
  - `test_credit_note_api_create.py` — POST /credit_notes/ from scratch
  - `test_credit_note_api_create_from_invoice.py` — admin action creates credit note with `corrects_invoice` + copied positions
  - `test_credit_note_api_list_filter.py` — filtering by contract, customer, status
  - `test_credit_note_api_permissions.py` — auth + role checks
  - `test_credit_note_admin_actions.py` — `create_credit_note` from contract; `create_credit_note_from_invoice` from invoice admin
  - `test_credit_note_accounting.py` — `register_credit_note_in_accounting` reverses Invoice booking direction

### Migrations

- `contracts/migrations/0004_rename_sales_document_to_commercial_document.py`
  - `RenameModel('SalesDocument' → 'CommercialDocument')`
  - `RenameModel` for all satellite models (`SalesDocumentPosition`, `TextParagraphInSalesDocument`, `PostalAddressForSalesDocument`, `EmailAddressForSalesDocument`, `PhoneAddressForSalesDocument`, `SalesDocumentMedia`)
  - `AlterModelTable` for every renamed model to rename the DB table
  - `RenameField('commercialdocument', 'derived_from_sales_document', 'derived_from_commercial_document')`
  - `RenameField` on every satellite model whose FK column was named `sales_document_id` → `commercial_document_id`
- `contracts/migrations/0005_add_credit_note.py`
  - `CreateModel('CreditNote', ...)` as a multi-table-inherited child of `CommercialDocument`

### Out of scope for PR #1

- Subclass document renames (`Quote` → `Quotation`, `DeliveryNote` → `DespatchAdvice`, `PurchaseConfirmation` → `SalesOrder`). Those are PR #2.
- Any component-level UBL rename (`Position` → `LineItem`, `PostalAddress` → `Address`, `ProductType` → `Item`). Defer until UBL import/export is concretely on the roadmap.

### Acceptance criteria

- `python manage.py migrate contract_object_management` runs clean on a fresh DB **and** on a DB that has already applied `0003_add_sales_document_media`.
- `grep -ri "sales_document\|SalesDocument\|salesdocument"` returns **zero** hits in `koalixcrm/contracts/` and `koalixcrm/contracts_api_py/` (some historical hits may remain in migrations `0001`–`0003` — those are intentional and must not be edited).
- Full pytest suite passes.
- Admin works end-to-end: create contract → add positions → create credit note from contract action → create credit note from invoice action (with populated positions + `corrects_invoice`) → PDF export → register in accounting.
- REST API round-trip: `POST /api/credit-notes/`, `GET /api/credit-notes/?contract=<id>`, admin action creates credit note visible via API.

---

## PR #2 — UBL 2.3 document-type alignment

### Goal
Rename the concrete document subclasses to match UBL 2.3 terminology where it disambiguates cleanly.

### Scope — rename

| Current | UBL 2.3 | New Django name | Notes |
|---|---|---|---|
| `Quote` | `Quotation` | `Quotation` | Clean rename. |
| `PurchaseConfirmation` | `Order` (sales side) | `SalesOrder` | Pure UBL "Order" collides with `PurchaseOrder` in Python namespace — keep `SalesOrder` for clarity. |
| `DeliveryNote` | `DespatchAdvice` | `DespatchAdvice` | More accurate than "delivery note". |
| `Invoice` | `Invoice` | `Invoice` | Unchanged. |
| `PaymentReminder` | `Reminder` | **`PaymentReminder` (keep)** | Bare `Reminder` is too generic in a CRM (tasks, appointments may also be reminders later). |
| `PurchaseOrder` | `Order` (buy side) | `PurchaseOrder` (keep) | See collision above. |
| *(added in PR #1)* `CreditNote` | `CreditNote` | `CreditNote` | Unchanged. |

### Ripple per renamed model (each is ~10 files)

- `contracts/models/<name>.py` — rename file + class + `db_table`
- `contracts/admin/<name>_admin.py` — rename file + `Option<Name>` + `Inline<Name>` classes
- `contracts/factory/<name>_factory.py` — rename file + `Standard<Name>Factory`
- `contracts/serializers/<name>_serializer.py` — rename file + serializer class
- `contracts/views/<name>_view_set.py` — rename file + viewset class
- `contracts_api_py/dto/<name>.py` — rename file + DTO
- `contracts_api_py/contracts_api.py` — update `__all__`
- `contracts_api_py/contracts_api_client.py` — rename endpoint methods
- `contracts/models/__init__.py`, `contracts/admin/__init__.py`, `contracts/factory/__init__.py` — update re-exports
- Admin actions that reference the old class (e.g. `create_quote` → `create_quotation`, `create_delivery_note` → `create_despatch_advice`)
- Templates in `crm/static/default_templates/**/*.xsl` that are named `quote.xsl`, `deliveryorder.xsl`, `purchaseconfirmation.xsl`

### Migrations

- One migration per renamed model:
  - `RenameModel('Quote' → 'Quotation')` + `AlterModelTable('crm_quote' → 'crm_quotation')`
  - `RenameModel('PurchaseConfirmation' → 'SalesOrder')` + `AlterModelTable('crm_purchaseconfirmation' → 'crm_salesorder')`
  - `RenameModel('DeliveryNote' → 'DespatchAdvice')` + `AlterModelTable('crm_deliverynote' → 'crm_despatchadvice')`
- Squash into a single `0006_ubl_document_rename.py` to keep the history tight.

### REST endpoint renames (breaking change for API consumers)

- `/api/quotes/` → `/api/quotations/`
- `/api/purchase-confirmations/` → `/api/sales-orders/`
- `/api/delivery-notes/` → `/api/despatch-advices/`
- Strategy: keep old routes for **one deprecation window** (e.g., 1 release) with a `DeprecationWarning` header, then remove. Decision to be confirmed when this PR is opened.

### Acceptance criteria

- `python manage.py migrate` clean on fresh DB and on DB that has applied PR #1.
- All admin URLs, REST endpoints, and factory imports work with the new names.
- Full pytest suite passes.
- Changelog entry lists all renames + API deprecation plan.

### Out of scope for PR #2

- Component-level UBL renames (Phase 3 below).
- Any data-model change (e.g., splitting `Customer`/`Supplier` into `Party` with role). That is a real refactor, not a rename, and needs its own RFC.

---

## Phase 3 (not planned yet — for future discussion)

Deferred until a concrete UBL import/export goal materializes:

- `Position` → `LineItem`
- `PostalAddress` → `Address`
- `ProductType` → `Item`
- `Unit` → `UnitCode`
- `Tax` → `TaxCategory` / `TaxScheme`
- Introduce `PaymentTerms` model (currently implicit on customer billing cycle).
- Introduce `Party` abstraction (large — affects `Customer`, `Supplier`, `Contact`, address/email/phone satellite models).

These cut across `crm/`, `products/`, `settings/`, `accounting/` — much wider blast radius than PR #1 and PR #2, and are data-model changes rather than pure renames.

---

## GitHub issues — to be created

1. **Issue #1:** _Rename `SalesDocument` → `CommercialDocument` and add `CreditNote` model_ — body = PR #1 section above.
2. **Issue #2:** _UBL 2.3 document-type alignment (`Quote`→`Quotation`, `PurchaseConfirmation`→`SalesOrder`, `DeliveryNote`→`DespatchAdvice`)_ — body = PR #2 section above, blocked by Issue #1.
