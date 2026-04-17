import logging
import os

import django

from koalixcrm_microservices.celery_app import app
from koalixcrm_mq_commands import PDFExportCommand
from koalixcrm_utils.aws_clients import get_s3_client

logger = logging.getLogger(__name__)

# Bootstrap Django ORM for the Celery worker so models can be imported
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projectsettings.settings.development_docker_settings')
django.setup()


def _update_process_status(process_id: int, status: str, result_url: str = "", error_message: str = ""):
    """Update the PDFExportProcess status via Django ORM."""
    from koalixcrm.core.models.pdf_export_process import PDFExportProcess
    try:
        process = PDFExportProcess.objects.get(id=process_id)
        process.status = status
        if result_url:
            process.result_url = result_url
        if error_message:
            process.error_message = error_message
        process.save()
    except PDFExportProcess.DoesNotExist:
        logger.error(f"PDFExportProcess {process_id} not found")


def _upload_to_s3(local_path: str, s3_key: str) -> str:
    """Upload a file to S3 and return the S3 URL."""
    bucket = os.getenv("S3_PDF_BUCKET", "koalixcrm-pdf-exports")
    s3 = get_s3_client()
    s3.upload_file(local_path, bucket, s3_key, ExtraArgs={"ContentType": "application/pdf"})

    s3_endpoint = os.getenv("S3_ENDPOINT_URL")
    if s3_endpoint:
        return f"{s3_endpoint}/{bucket}/{s3_key}"
    else:
        region = os.getenv("AWS_REGION", "eu-west-3")
        return f"https://{bucket}.s3.{region}.amazonaws.com/{s3_key}"


def _resolve_source_object(source_model: str, source_id: int):
    """Resolve the Django model instance from model name and ID."""
    from koalixcrm.contracts.models.commercial_document import CommercialDocument
    from koalixcrm.contracts.models.invoice import Invoice
    from koalixcrm.contracts.models.quote import Quote
    from koalixcrm.contracts.models.delivery_note import DeliveryNote
    from koalixcrm.contracts.models.purchase_order import PurchaseOrder
    from koalixcrm.contracts.models.purchase_confirmation import PurchaseConfirmation
    from koalixcrm.contracts.models.payment_reminder import PaymentReminder
    from koalixcrm.contracts.models.credit_note import CreditNote

    MODEL_MAP = {
        'CommercialDocument': CommercialDocument,
        'Invoice': Invoice,
        'Quote': Quote,
        'DeliveryNote': DeliveryNote,
        'PurchaseOrder': PurchaseOrder,
        'PurchaseConfirmation': PurchaseConfirmation,
        'PaymentReminder': PaymentReminder,
        'CreditNote': CreditNote,
    }

    model_class = MODEL_MAP.get(source_model)
    if not model_class:
        raise ValueError(f"Unknown source model: {source_model}")

    return model_class.objects.get(id=source_id)


@app.task(
    name="koalixcrm_microservices.pdf_export_task.tasks.run",
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=30,
    max_retries=3,
)
def run(payload: dict) -> dict:
    """
    Execute PDF generation via FOP and upload result to S3.

    Steps:
    1. Parse command
    2. Update process status to 'processing'
    3. Resolve source object and template set
    4. Call create_pdf (FOP transformation)
    5. Upload PDF to S3
    6. Update process status to 'completed' with result URL
    """
    cmd = PDFExportCommand.from_dict(payload)
    logger.info(f"Starting PDF export for process {cmd.process_id}, "
                f"model={cmd.source_model}, id={cmd.source_id}")

    _update_process_status(cmd.process_id, 'processing')

    try:
        from django.contrib.auth.models import User
        from koalixcrm.djangoUserExtension.models import DocumentTemplate
        from koalixcrm.contracts.models.commercial_document import CommercialDocument
        from koalixcrm.contracts.models.commercial_document_media import CommercialDocumentMedia

        source_obj = _resolve_source_object(cmd.source_model, cmd.source_id)
        template_set = DocumentTemplate.objects.get(id=cmd.template_set_id)
        printed_by = User.objects.get(id=cmd.printed_by_user_id)

        # Run the FOP-based PDF creation (CPU-intensive)
        pdf_path = source_obj.create_pdf(template_set, printed_by)

        # Upload to S3
        s3_key = f"pdf-exports/{cmd.source_model}_{cmd.source_id}_{cmd.process_id}.pdf"
        result_url = _upload_to_s3(pdf_path, s3_key)

        # Resolve the base CommercialDocument for the FK (handles STI subclasses)
        base_doc = CommercialDocument.objects.get(id=source_obj.id)

        # Create CommercialDocumentMedia record following the S3Media pattern
        CommercialDocumentMedia.objects.create(
            commercial_document=base_doc,
            s3_url=result_url,
            s3_key=s3_key,
            status='completed',
            media_type='application/pdf',
            pdf_export_process_id=cmd.process_id,
            created_by=printed_by,
        )

        _update_process_status(cmd.process_id, 'completed', result_url=result_url)
        logger.info(f"PDF export completed for process {cmd.process_id}: {result_url}")

        return {"status": "completed", "process_id": cmd.process_id, "result_url": result_url}

    except Exception as e:
        error_msg = str(e)
        logger.exception(f"PDF export failed for process {cmd.process_id}: {error_msg}")
        _update_process_status(cmd.process_id, 'failed', error_message=error_msg)
        raise


@app.task(name="koalixcrm_microservices.pdf_export_task.tasks.health_check")
def health_check():
    logger.info("PDF export worker health check OK")
    return {"status": "ok"}
