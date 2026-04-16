# PDF Creation Microservice

The PDF Creation Microservice is a Celery-based worker that asynchronously renders
commercial documents (Invoice, Quote, Delivery Note, Purchase Order, Purchase
Confirmation, Payment Reminder, Credit Note) into PDF files using Apache FOP.

It is decoupled from the Django monolith via an AWS SQS queue and stores the
generated PDFs in S3.

## When is the service triggered?

A PDF export is triggered when a **Django admin action** (`create_pdf_async`) is
executed on a `CommercialDocument` (or any of its subclasses) in the Django admin UI.

Trigger chain (producer side):

1. Admin user selects one or more commercial documents and runs the
   `create_pdf_async` action
   (`koalixcrm/contracts/admin/commercial_document_admin.py:231-256`).
2. A `PDFExportProcess` record is created in Django with status `pending`
   (`koalixcrm/core/models/pdf_export_process.py:8-91`).
3. A `post_save` signal (`koalixcrm/core/signals/pdf_export_signals.py:14-41`)
   serializes a `PDFExportCommand` envelope and pushes it onto SQS
   (`KOALIXCRM_MICROSERVICE_SQS`).
4. The microservice picks up the message, renders the PDF, and stores the result.

## Interfaces at a glance

| Interface | Direction | Purpose |
| --- | --- | --- |
| **AWS SQS** | Inbound | Receives `PDFExportCommand` envelopes from Django producer |
| **Django ORM (shared DB)** | Bidirectional | Reads `CommercialDocument`, `DocumentTemplate`, `User`; writes `PDFExportProcess` status and `CommercialDocumentMedia` |
| **AWS S3 – template bucket** | Read | Downloads XSL, FOP config, and logo files referenced by `DocumentTemplate` |
| **AWS S3 – PDF export bucket** (`S3_PDF_BUCKET`) | Write | Uploads the rendered PDF |
| **Apache FOP CLI** | Outbound subprocess | Performs XSL-FO → PDF transformation (`/usr/bin/fop`) |

> ⚠️ Note on the originally assumed "CRUD REST interface": the worker does **not**
> talk to Django via REST. Django and the worker share the same database, and the
> worker uses the Django ORM directly (the Celery worker bootstraps Django at
> startup — see `koalixcrm_microservices/pdf_export_task/tasks.py:14-15`).

## Documents in this folder

| File | Content |
| --- | --- |
| [`01-context.md`](./01-context.md) | C4-style context diagram (external actors & systems) |
| [`02-architecture.md`](./02-architecture.md) | Component/container architecture diagram |
| [`03-use-case-flow.md`](./03-use-case-flow.md) | Use case and end-to-end sequence flow |
| [`04-state-machine.md`](./04-state-machine.md) | `PDFExportProcess` status lifecycle |
| [`05-interfaces.md`](./05-interfaces.md) | Interface details (SQS envelope wire contract, S3 layout, FOP CLI invocation, env vars) |
| [`10-migration-reference.md`](./10-migration-reference.md) | Source-of-truth map for the Java rewrite: files to mirror, delete, keep; OIDC env vars; retry semantics; deletion checklist |
| [`11-dto-shapes.md`](./11-dto-shapes.md) | JSON DTO sketches the new Django endpoints must return (stage 1 anchor) |

## High-level processing steps inside the microservice

Source of truth: `koalixcrm_microservices/pdf_export_task/tasks.py:76-141`.

1. **Receive** `PDFExportCommand` envelope from SQS (poller thread
   `koalixcrm_microservices/sqs_poller.py`).
2. **Dispatch** to the Celery task `koalixcrm_microservices.pdf_export_task.tasks.run`.
3. **Parse** the command payload into a `PDFExportCommand` dataclass.
4. **Set status** `PDFExportProcess.status = 'processing'`.
5. **Resolve** the source object (Invoice / Quote / …) via `MODEL_MAP`, the
   `DocumentTemplate`, and the triggering `User`.
6. **Render PDF** by calling `source_obj.create_pdf(template_set, printed_by)`
   which:
   - downloads the XSL, FOP config, and logo from S3 into a temp dir,
   - serializes the document to XML,
   - invokes `fop -c <cfg> -xml <xml> -xsl <xsl> -pdf <out>` as a subprocess.
7. **Upload** the rendered PDF to S3 at
   `pdf-exports/<model>_<id>_<process_id>.pdf`.
8. **Create** a `CommercialDocumentMedia` row referencing the S3 object.
9. **Set status** `PDFExportProcess.status = 'completed'` with `result_url`.
10. **On error**: Celery retries up to 3 times with exponential backoff; final
    failure sets status `failed` with `error_message`.
