# Migration Reference — source-of-truth map

Companion to [`CELERY_TO_JAVA_MIGRATION.md`](../../CELERY_TO_JAVA_MIGRATION.md)
and tracking issue
[#386](https://github.com/KoalixSwitzerland/koalixcrm/issues/386). This file
pins the exact locations in the current code that are the **specification**
for the Java rewrite. Keep it up-to-date as stages land.

## Scope boundary — what the Java service handles

The Java service **only handles commercial documents** (the closed set below).
The `serialize_to_xml()` / `create_pdf()` methods on `accounting_period`,
`account`, `reporting_period`, `project`, `task`, `human_resource`, `work`
are **out of scope** for this migration — they remain synchronous
Django-rendered paths for now and should be considered in a later migration.

Closed set of supported `source_model` values (from
`koalixcrm_microservices/pdf_export_task/tasks.py:58-67`):

```
CommercialDocument, Invoice, Quote, DeliveryNote, PurchaseOrder,
PurchaseConfirmation, PaymentReminder, CreditNote
```

Only these get Java `XmlBuilder<T>` implementations in stage 3.

## Spec: `serialize_to_xml()` methods (in scope)

Each Java `XmlBuilder<T>` must produce **byte-equivalent** output to its
Python counterpart (subject to whitespace). Source methods:

| Model | File:line |
| --- | --- |
| `CommercialDocument` (base) | `koalixcrm/contracts/models/commercial_document.py:115-141` |

> At the time of writing, the contract subclasses (Invoice, Quote, …) do not
> override `serialize_to_xml`; they inherit the base. Confirm during stage 3 —
> if per-subclass XML differs, add overrides to the inventory here.

Merge logic that combines document + template + user-extension XML into the
final XSL-FO input lives in
`koalixcrm/core/documents/pdf_export.py:116-120`. The Java `XmlAggregator`
mirrors that structure.

Out-of-scope methods (listed for awareness, not for rewrite):

- `koalixcrm/reporting/models/work.py:63`
- `koalixcrm/reporting/models/project.py:99`
- `koalixcrm/reporting/models/task.py:348`
- `koalixcrm/reporting/models/human_resource.py:21`
- `koalixcrm/reporting/models/reporting_period.py:164`
- `koalixcrm/accounting/models/accounting_period.py:94`
- `koalixcrm/accounting/models/account.py:89`

## Spec: `create_pdf()` methods (to delete in stage 5 — in-scope paths only)

| Method | File:line | Action |
| --- | --- | --- |
| `CommercialDocument.create_pdf` | `koalixcrm/contracts/models/commercial_document.py:182-185` | **Delete** |
| Admin action `create_pdf` (sync) | `koalixcrm/contracts/admin/commercial_document_admin.py:219-229` | **Delete** (decision A) |
| Admin action `create_pdf_async` | `koalixcrm/contracts/admin/commercial_document_admin.py:231-256` | **Keep** — the entry point for the Java service |
| `PDFExportView.export_pdf` sync view | `koalixcrm/core/views/pdfexport.py` (referenced from admin:220) | **Delete** |
| `PDFExport.create_pdf` | `koalixcrm/core/documents/pdf_export.py:99-151` | **Delete** |
| `XSLFORenderer` | `koalixcrm/core/views/renderer.py:17` | **Delete** |

Out-of-scope `create_pdf()` methods (stay, for now):
`accounting_period.py:58`, `reporting_period.py:150`, `project.py:65`,
`human_resource.py:175`, and the accounting-specific admin actions at
`accounting_period.py:226` and `:238`.

## Django producer (stays)

| Component | File:line | Notes |
| --- | --- | --- |
| `create_pdf_async` admin action | `koalixcrm/contracts/admin/commercial_document_admin.py:231-256` | Creates `PDFExportProcess(status='pending', source_model, source_id, template_set, triggered_by)`. |
| `PDFExportProcess` model | `koalixcrm/core/models/pdf_export_process.py:8-90` | Status choices: `pending` / `processing` / `completed` / `failed`. Table `crm_pdfexportprocess`. |
| `post_save` signal | `koalixcrm/core/signals/pdf_export_signals.py:14-41` | Builds `PDFExportCommand` and calls `queue.send_message(MessageBody=body)`. On failure sets `status='failed'` + `error_message`. |
| `PDFExportCommand` envelope | `koalixcrm_mq_commands/pdf_export_command.py:8-63` | 5 fields (see [`05-interfaces.md`](./05-interfaces.md#sqs-envelope---wire-contract)). |

The signal continues to use the Python envelope class (producer stays in
Python). Only consumers move to Java.

## OIDC / M2M auth — exact env var names to reuse

Source: `koalixcrm/shared/api_client.py:55-65, 194`. These are the names the
Java `OidcTokenProvider` **must** use for ops parity:

| Env var | Purpose |
| --- | --- |
| `CELERY_WORKER_M2M_CLIENT_ID` | OIDC client id |
| `CELERY_WORKER_M2M_CLIENT_SECRET` | OIDC client secret |
| `CELERY_WORKER_M2M_OIDC_ISSUER` | OIDC issuer — Java does `${issuer}/.well-known/openid-configuration` discovery, then POSTs `grant_type=client_credentials` to the discovered `token_endpoint` |
| `CELERY_WORKER_M2M_SCOPE` | optional scope attached to the token request |
| `KOALIXCRM_API_URL` | base URL of the Django API |
| `X_CUSTOM_ORIGIN_VERIFICATION_ON` | `"true"`/`"false"` |
| `X_CUSTOM_ORIGIN_VERIFICATION_KEY` | value of the `X-Custom-Origin-Verify` header when enabled |
| `KOALIXCRM_TOKEN_SAVE_TO_ENV` | leave default; not needed by Java |

The *names* have `CELERY_WORKER_` in them only for historical reasons — the
Java service must keep them unchanged to avoid an env-var migration in ops.
(If renamed later, that's a separate change.)

Retry on 401/403: `api_client.py:323-334` refreshes the token and retries
once. Java should mirror: one retry with fresh token on 401/403, then fail.

## Existing Django REST surface — what stage 1 extends

From the earlier survey:

- Router: `projectsettings/urls.py:48` uses `rest_framework.routers.DefaultRouter()`.
- Base class: `koalixcrm/shared/base_model_view_set.py` (`BaseModelViewSet`,
  `IsAuthenticated + ModelPermissionsWithListView`).
- Existing commercial-document ViewSets (shallow JSON today — stage 1 adds
  **nested** serializers):
  - `koalixcrm/contracts/views/invoice_view_set.py`
  - `koalixcrm/contracts/views/quotation_view_set.py`
  - `koalixcrm/contracts/views/purchase_order_view_set.py`
  - `koalixcrm/contracts/views/despatch_advice_view_set.py` *(DeliveryNote)*
  - `koalixcrm/contracts/views/payment_reminder_view_set.py`
  - `koalixcrm/contracts/views/credit_note_view_set.py`
- Missing (stage 1 creates):
  - `PDFExportProcessViewSet` (GET detail, PATCH)
  - `DocumentTemplateViewSet` (GET detail, + detail actions `xsl/`,
    `fop-config/`, `logo/` → 302 presigned S3 URL)
  - `CommercialDocumentMediaViewSet` (POST create)
  - `UserExtensionViewSet` (GET detail)

Permissions: `koalixcrm/shared/permissions.py:8` (`ModelPermissionsWithListView`).
Grant the M2M client the necessary model permissions in Django.

## S3 layout (unchanged)

- **Templates bucket** (shared with Django app via `TemplateFileStorage`):
  paths are whatever `DocumentTemplate.{xsl_file, fop_config_file, logo}`
  `FileField`s resolve to. Java never addresses these directly — it only
  follows the 302 redirect from the template endpoints.
- **PDF export bucket**: env `S3_PDF_BUCKET` (default `koalixcrm-pdf-exports`).
- **PDF object key format** (from
  `koalixcrm_microservices/pdf_export_task/tasks.py:115`):
  ```
  pdf-exports/<source_model>_<source_id>_<process_id>.pdf
  ```
  Java must preserve this format — downstream consumers rely on it.
- **Result URL format** (from `tasks.py:39-44`): `${S3_ENDPOINT_URL}/${bucket}/${key}`
  when endpoint is set (local/MinIO), else
  `https://${bucket}.s3.${AWS_REGION}.amazonaws.com/${key}`.

## Retry semantics to mirror

Source: `koalixcrm_microservices/pdf_export_task/tasks.py:76-82`.

```
autoretry_for   = (Exception,)
retry_backoff   = True          # exponential
retry_backoff_max = 30          # seconds cap
max_retries     = 3
```

Java equivalent via Spring Retry: `@Retryable(maxAttempts=3, backoff=@Backoff(delay=1000, multiplier=2, maxDelay=30000))` around the orchestrator. Terminal failure → `PATCH /api/pdf-export-processes/{id}/` with `status='failed'`, `error_message=<exception>` and let the SQS message go to the DLQ.

## Deletion checklist for stage 5

Concrete paths — do not delete earlier stages of code until stage 5:

```
koalixcrm_microservices/                       # whole package
koalixcrm_mq_commands/                         # whole package
koalixcrm/core/documents/pdf_export.py
koalixcrm/core/views/renderer.py               # XSLFORenderer
koalixcrm/core/views/pdfexport.py              # sync PDFExportView
koalixcrm/contracts/models/commercial_document.py        # remove methods:
                                               #   create_pdf, serialize_to_xml
koalixcrm/contracts/admin/commercial_document_admin.py   # remove sync action
                                               #   create_pdf (keep async)
docker/requirements/celery.txt
docker/dev/Dockerfile.celery
docker/prod/Dockerfile.celery
.github/workflows/docker-celery.yml            # or rename → docker-pdf-service.yml
```

Verification commands:

```bash
grep -R "serialize_to_xml\|XSLFORenderer\|PDFExportView\|PDFExport\.create_pdf" \
    koalixcrm/contracts koalixcrm/core     # must be empty
test ! -d koalixcrm_microservices && test ! -d koalixcrm_mq_commands
```

## Golden-PDF capture (stage 3 prep)

While the Python worker is still alive on `develop`, capture deterministic
reference PDFs to diff against the Java output:

1. In a `conftest.py` fixture or a one-shot script, freeze `datetime.now()`
   (e.g. via `freezegun`) and any random IDs.
2. For each of the 7 in-scope commercial-document types, run the current
   flow (admin action → SQS → Python worker → S3) against a curated seed
   dataset.
3. Copy the resulting PDFs from S3 into
   `tests/fixtures/golden_pdfs/<model>/<seed_name>.pdf` and commit.
4. In stage 3, assert the Java output matches either byte-for-byte (after
   deterministic-date patching) or via structural comparison with Apache
   PDFBox text-extract.

Seed dataset suggestion: one minimal invoice, one multi-line invoice with
taxes, one delivery note, one quote with discounts, one payment reminder,
one purchase order, one purchase confirmation, one credit note.

## Decisions log (cross-ref)

Already recorded in `CELERY_TO_JAVA_MIGRATION.md` under "Decisions recorded".
Short-form table here for quick lookup:

| Topic | Decision |
| --- | --- |
| Runtime | Spring Boot 3 + Spring Cloud AWS v3 `@SqsListener` |
| Apache FOP | Library (in-process), not subprocess |
| XML strategy | StAX `XMLStreamWriter`, one `XmlBuilder<T>` per DTO |
| API boundary | Django JSON-only; all XML in the Java worker |
| Sync PDF path | Deleted (option A) |
| Auth | OIDC M2M `client_credentials`, reuse existing env-var names |
| Template assets | 302 → presigned S3 URL |
| Client library | Hand-written `app_api_java` (not OpenAPI-generated) |
| Gradle/Maven | Gradle Kotlin DSL, JDK 21, `eclipse-temurin:21-jre-alpine` runtime |
| Dev parity | ElasticMQ + MinIO via Spring Cloud AWS `endpoint` properties |
