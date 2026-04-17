# Use Case & End-to-End Flow

## Use case diagram

```mermaid
flowchart TB
    User(("Back-Office User"))
    Recipient(("Document Recipient"))
    Ops(("Ops / SRE"))

    subgraph System["PDF Creation Microservice (System Boundary)"]
        UC1(["UC1 — Trigger PDF export<br/>for a commercial document"])
        UC2(["UC2 — Track export status"])
        UC3(["UC3 — Render PDF asynchronously<br/>(XSL-FO → PDF via FOP)"])
        UC4(["UC4 — Store PDF in S3"])
        UC5(["UC5 — Link rendered PDF<br/>to the source document"])
        UC6(["UC6 — Download rendered PDF"])
        UC7(["UC7 — Observe worker health<br/>(health_check task)"])
    end

    User --> UC1
    User --> UC2
    Recipient --> UC6
    Ops --> UC7

    UC1 -.->|«include»| UC3
    UC3 -.->|«include»| UC4
    UC4 -.->|«include»| UC5
    UC2 -.->|«extend»| UC5
```

### Primary use case — UC1 "Trigger PDF export"

| | |
| --- | --- |
| **Actor** | Back-Office User |
| **Precondition** | User is authenticated and has the admin permission on the target `CommercialDocument` subclass; at least one `DocumentTemplate` exists. |
| **Trigger** | User selects documents in the Django admin change-list and runs the `create_pdf_async` action. |
| **Main success scenario** | 1. A `PDFExportProcess` is created with status `pending`.<br/>2. A `PDFExportCommand` envelope is enqueued on SQS.<br/>3. The microservice consumes the message and renders the PDF.<br/>4. The PDF is uploaded to S3.<br/>5. A `CommercialDocumentMedia` entry is created and `PDFExportProcess.status = completed` with a `result_url`. |
| **Alternative flows** | *A1.* SQS `SendMessage` fails → process status is set directly to `failed` in the signal handler.<br/>*A2.* Celery task raises → autoretry up to 3 times with backoff, then `failed` with `error_message`. |
| **Postcondition** | A PDF is reachable via `result_url`, and `CommercialDocumentMedia` links it to the source document. |

## End-to-end sequence flow

```mermaid
sequenceDiagram
    autonumber
    actor U as Back-Office User
    participant A as Django Admin<br/>(CommercialDocumentAdmin)
    participant P as PDFExportProcess<br/>(model)
    participant S as post_save signal<br/>(pdf_export_signals)
    participant Q as SQS Queue<br/>(KOALIXCRM_MICROSERVICE_SQS)
    participant PO as SQS Poller<br/>(daemon thread)
    participant C as Celery task<br/>tasks.run
    participant R as PDFExport.create_pdf
    participant T as S3 (templates)
    participant F as Apache FOP CLI
    participant PDFS3 as S3 (S3_PDF_BUCKET)
    participant M as CommercialDocumentMedia
    actor Recv as Document Recipient

    U->>A: Select docs + "Create PDF (async)"
    A->>P: create(status=pending,<br/>source_model, source_id,<br/>template_set, triggered_by)
    P-->>S: post_save(created=True)
    S->>S: Build PDFExportCommand envelope
    S->>Q: SendMessage (JSON)
    alt SendMessage fails
        S->>P: status = "failed",<br/>error_message = …
        S-->>A: show error in admin
    else SendMessage ok
        S-->>A: "Export queued"
    end

    loop Long-poll loop
        PO->>Q: ReceiveMessage
        Q-->>PO: PDFExportCommand envelope
        PO->>C: celery_app.send_task("pdf_export_task.tasks.run", [payload])
        PO->>Q: DeleteMessage
    end

    C->>P: status = "processing"
    C->>C: resolve source_obj via MODEL_MAP<br/>(Invoice/Quote/…)
    C->>R: source_obj.create_pdf(template_set, printed_by)
    R->>T: download xsl / fop_config / logo
    R->>R: serialize doc+template to XML
    R->>F: subprocess: fop -c cfg -xml doc.xml<br/>-xsl tpl.xsl -pdf out.pdf
    F-->>R: out.pdf
    R-->>C: local PDF path

    C->>PDFS3: PutObject pdf-exports/<model>_<id>_<pid>.pdf
    PDFS3-->>C: 200 OK
    C->>M: create(s3_url, s3_key, status=completed,<br/>media_type="application/pdf",<br/>pdf_export_process=…, created_by=…)
    C->>P: status = "completed",<br/>result_url = <S3 URL>

    Recv->>PDFS3: GET result_url
    PDFS3-->>Recv: application/pdf
```

### Error / retry paths

```mermaid
sequenceDiagram
    autonumber
    participant C as Celery task (tasks.run)
    participant P as PDFExportProcess
    participant CB as Celery broker (SQS)

    Note over C: autoretry_for=(Exception,)<br/>retry_backoff=True<br/>retry_backoff_max=30s<br/>max_retries=3

    C-->>C: Exception raised<br/>(e.g. FOP failed, S3 down)
    C->>P: status = "failed",<br/>error_message = str(e)
    C->>CB: retry scheduled (exp backoff)
    alt retries < 3 and transient error
        CB-->>C: redeliver message
        C->>P: status = "processing"
        Note right of C: attempt pipeline again
    else retries exhausted
        C-->>CB: task marked failed
        Note right of P: status remains "failed"
    end
```
