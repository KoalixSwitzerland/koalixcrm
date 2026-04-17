# Context Diagram

Shows the PDF Creation Microservice in the context of its users and the
surrounding systems it integrates with.

```mermaid
C4Context
    title System Context — PDF Creation Microservice

    Person(admin, "Back-Office User", "Creates invoices, quotes,<br/>delivery notes; triggers<br/>'create_pdf_async' admin action")
    Person(recipient, "Document Recipient", "Customer / supplier<br/>receiving the PDF<br/>(via download link)")

    System_Boundary(koalix, "koalixCRM Platform") {
        System(django, "koalixCRM (Django)", "Business logic, admin UI,<br/>commercial documents,<br/>producer of PDF export commands")
        System(pdfms, "PDF Creation Microservice", "Celery worker — asynchronously<br/>renders commercial documents<br/>to PDF using Apache FOP")
    }

    System_Ext(sqs, "AWS SQS", "Command queue<br/>(KOALIXCRM_MICROSERVICE_SQS)")
    System_Ext(s3tpl, "AWS S3 – Templates", "Stores XSL-FO templates,<br/>FOP configs, logos")
    System_Ext(s3pdf, "AWS S3 – PDF Exports", "Stores rendered PDFs<br/>(S3_PDF_BUCKET)")
    System_Ext(db, "PostgreSQL / RDS", "Shared relational database<br/>(CommercialDocument,<br/>PDFExportProcess, …)")
    System_Ext(fop, "Apache FOP CLI", "XSL-FO → PDF renderer<br/>(/usr/bin/fop)")

    Rel(admin, django, "Runs 'create_pdf_async'<br/>admin action", "HTTPS")
    Rel(django, sqs, "Sends PDFExportCommand", "JSON over SQS")
    Rel(django, db, "CRUD (ORM)", "SQL")

    Rel(pdfms, sqs, "Polls for commands", "SQS long-poll")
    Rel(pdfms, db, "Reads document &<br/>writes status / media", "SQL (Django ORM)")
    Rel(pdfms, s3tpl, "Downloads XSL,<br/>FOP config, logo", "HTTPS")
    Rel(pdfms, s3pdf, "Uploads rendered PDF", "HTTPS")
    Rel(pdfms, fop, "XSL-FO → PDF", "subprocess")

    Rel(recipient, s3pdf, "Downloads PDF<br/>(via result_url)", "HTTPS")

    UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="1")
```

## Actors

| Actor | Role |
| --- | --- |
| **Back-Office User** | Internal user with Django admin access who selects commercial documents and triggers the `create_pdf_async` action. |
| **Document Recipient** | External customer/supplier who receives the link to the rendered PDF stored in S3. |

## External systems

| System | Purpose |
| --- | --- |
| **AWS SQS** | Decouples producer (Django) from consumer (microservice). Single queue, configured via `KOALIXCRM_MICROSERVICE_SQS`. |
| **AWS S3 (Templates)** | Holds the XSL-FO templates, FOP config, and logo files referenced by `DocumentTemplate`. Backed by Django `TemplateFileStorage`. |
| **AWS S3 (PDF Exports)** | Destination bucket for rendered PDFs. Bucket name configured via `S3_PDF_BUCKET`. |
| **PostgreSQL / RDS** | Shared database between Django and the microservice. The microservice uses the Django ORM via `django.setup()` rather than a REST API. |
| **Apache FOP CLI** | Java-based XSL-FO processor invoked as a subprocess at `/usr/bin/fop` (configurable via `FOP_EXECUTABLE`). |
