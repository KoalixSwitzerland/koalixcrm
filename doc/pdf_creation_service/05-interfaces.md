# Interfaces

Detailed contracts of every external touchpoint of the PDF Creation
Microservice.

## 1. SQS — command intake

- **Queue**: env var `KOALIXCRM_MICROSERVICE_SQS` (default `koalixcrm-microservice-sqs`).
- **Direction**: Django producer → microservice consumer.
- **Poller**: `koalixcrm_microservices/sqs_poller.py` (`ReceiveMessage`,
  `MaxNumberOfMessages=5`, `WaitTimeSeconds=2`, `VisibilityTimeout=60`).
- **Local dev**: ElasticMQ via `SQS_ENDPOINT_URL` (see `elasticmq.conf`).

### SQS envelope — wire contract

> ⚓ **Stability contract.** This is the JSON the Django producer writes and
> the (current Python / future Java) consumer reads. Any change here is a
> coordinated release across producer and consumer. The Java
> `pdf-export-service` mirrors this shape 1:1 as a `PdfExportCommand`
> record. Source of truth: `koalixcrm_mq_commands/pdf_export_command.py:8-63`
> on the producer side.

```json
{
  "type": "PDFExportCommand",
  "payload": {
    "process_id": 42,
    "source_model": "Invoice",
    "source_id": 17,
    "template_set_id": 3,
    "printed_by_user_id": 5
  }
}
```

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `type` | string | yes | Must equal `"PDFExportCommand"`. Unknown types are logged and dropped (SQS message deleted) — see `sqs_poller.py:47`. |
| `payload.process_id` | int | yes | `PDFExportProcess.id`. The worker reads/writes this row. |
| `payload.source_model` | string | yes | One of the fixed set below. |
| `payload.source_id` | int | yes | PK of the source commercial document. |
| `payload.template_set_id` | int | yes | `DocumentTemplate.id`. **`0` means "not set"** — the producer signal substitutes `0` when `template_set` is null (`pdf_export_signals.py:28`). The worker treats `0` as an error. |
| `payload.printed_by_user_id` | int | yes | `auth.User.id` of the triggering admin. **`0` means "not set"** (same substitution, `pdf_export_signals.py:29`). |

Supported `source_model` values (closed set, matches `tasks.py:58-67`):
`CommercialDocument`, `Invoice`, `Quote`, `DeliveryNote`, `PurchaseOrder`,
`PurchaseConfirmation`, `PaymentReminder`, `CreditNote`.

Changing this set **requires** a coordinated change in both the producer
(`MODEL_MAP` was producer-side in the signal is implicit — any
`PDFExportProcess.source_model` value reaches the worker) and the Java
service's `XmlBuilder` registry.

## 2. Shared database (Django ORM)

The worker **does not** talk to Django over REST. It runs `django.setup()` at
import time (`tasks.py:14-15`) and uses the same ORM models. Relevant tables:

| Model | Table role for the worker |
| --- | --- |
| `PDFExportProcess` | Read by id, status/result_url/error_message are updated (`_update_process_status`, `tasks.py:18-30`). |
| `CommercialDocument` and subclasses (`Invoice`, `Quote`, `DeliveryNote`, `PurchaseOrder`, `PurchaseConfirmation`, `PaymentReminder`, `CreditNote`) | Read-only source for rendering. Subclass is resolved via `MODEL_MAP`. |
| `DocumentTemplate` | Read-only; exposes the XSL file, FOP config, and logo (all `FileField` backed by `TemplateFileStorage` → S3). |
| `User` (`auth_user`) | Read-only lookup of the user who triggered the export. |
| `CommercialDocumentMedia` | Inserted on success. |

Because the DB is shared, the microservice must be deployed with the same
database credentials and migration state as Django.

## 3. AWS S3 — templates bucket

- **Access**: read-only via Django `FileField.open()` (`TemplateFileStorage`).
- **Files** (per `DocumentTemplate`, `djangoUserExtension/models/document_template.py`):
  - `xsl_file` — XSL-FO stylesheet (required).
  - `fop_config_file` — FOP configuration XML (optional).
  - `logo` — image used inside the PDF (optional).
- `PDFExport.create_pdf` downloads these to a temp directory before invoking
  FOP (`koalixcrm/core/documents/pdf_export.py:99-151`).

## 4. AWS S3 — PDF exports bucket

- **Bucket**: env var `S3_PDF_BUCKET` (default `koalixcrm-pdf-exports`).
- **Access**: write-only by the worker (`_upload_to_s3`, `tasks.py:33-44`).
- **Key layout**:
  ```
  pdf-exports/<source_model>_<source_id>_<process_id>.pdf
  ```
- **Content-Type**: `application/pdf`.
- **Returned URL**: either `{S3_ENDPOINT_URL}/{bucket}/{key}` (local/MinIO) or
  `https://{bucket}.s3.{AWS_REGION}.amazonaws.com/{key}` (production).

## 5. Apache FOP CLI

- **Binary**: `/usr/bin/fop` (override with `settings.FOP_EXECUTABLE`).
- **Invocation** (`koalixcrm/core/documents/pdf_export.py:84-96`):
  ```bash
  fop -c <fop_config_path> \
      -xml <serialized_document_xml> \
      -xsl <template_xsl> \
      -pdf <output_pdf_path>
  ```
- Runs via `subprocess.run(...)`; non-zero exit is captured and re-raised as a
  `RuntimeError` that includes FOP's stderr — this propagates up to the Celery
  task and is persisted in `PDFExportProcess.error_message`.
- Requires a Java runtime in the worker container (FOP is a JVM tool).

## 6. No REST API on the worker

The microservice does not expose any HTTP endpoints. There is no Flask/FastAPI
server — only the Celery worker process, the SQS poller thread, and Celery
beat for periodic health-check tasks
(`celery_app.py:75-80`, task `pdf_export_task.tasks.health_check`).

## 7. Environment variables summary

| Variable | Used by | Default | Purpose |
| --- | --- | --- | --- |
| `CELERY_BROKER_URL` | Celery | — | SQS broker URL (`sqs://…`). |
| `CELERY_RESULT_BACKEND` | Celery | — | Result backend (optional). |
| `CELERY_SQS` | Celery | — | Default Celery queue name (task routing). |
| `KOALIXCRM_MICROSERVICE_SQS` | Poller + producer signal | `koalixcrm-microservice-sqs` | Command queue name. |
| `AWS_REGION` | All AWS clients | `eu-west-3` | AWS region. |
| `AWS_PROFILE` | Celery broker (when no endpoint) | — | AWS profile used to resolve account id. |
| `SQS_ENDPOINT_URL` | Celery + poller | — | Local ElasticMQ endpoint. |
| `S3_ENDPOINT_URL` | S3 uploader | — | Local MinIO endpoint; also used to build `result_url`. |
| `S3_PDF_BUCKET` | S3 uploader | `koalixcrm-pdf-exports` | Destination bucket. |
| `FOP_EXECUTABLE` | `PDFExport.create_pdf` | `/usr/bin/fop` | Path to FOP CLI. |
| `PDF_OUTPUT_ROOT` | `PDFExport.create_pdf` | `<STATIC_ROOT>/pdf` | Temp directory for FOP output. |
| `ENABLE_SQS_POLLER` | `celery_app.py:93-95` | `true` | Disables the poller thread when `false` (useful in tests). |
| `POLL_SLEEP_SECONDS` | `sqs_poller.py:59` | `2` | Sleep between empty polls. |
| `SQS_HEALTHCHECK_SECONDS` | Celery beat | `300` | Interval of the health-check task. |
| `LOG_LEVEL` | Celery app logger | `INFO` | Logging verbosity. |
| `DJANGO_SETTINGS_MODULE` | `tasks.py:14` | `projectsettings.settings.development_docker_settings` | Django settings module for the ORM bootstrap. |
