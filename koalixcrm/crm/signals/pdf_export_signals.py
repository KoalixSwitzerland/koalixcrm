"""
Signal for PDFExportProcess: on creation, send PDFExportCommand to SQS.
"""
import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from koalixcrm.crm.models.pdf_export_process import PDFExportProcess
from koalixcrm_mq_commands import PDFExportCommand
from koalixcrm_utils.aws_clients import get_sqs_queue

logger = logging.getLogger(__name__)


@receiver(post_save, sender=PDFExportProcess, dispatch_uid="pdf_export_signals.trigger_pdf_export")
def trigger_pdf_export(sender, instance, created, **kwargs):
    """
    Trigger PDF generation when a new PDFExportProcess is created.
    """
    if not created:
        return

    logger.info(f"Triggering PDF export for process {instance.id}")

    command = PDFExportCommand(
        process_id=instance.id,
        source_model=instance.source_model,
        source_id=instance.source_id,
        template_set_id=instance.template_set_id if instance.template_set else 0,
        printed_by_user_id=instance.triggered_by_id if instance.triggered_by else 0,
    )

    try:
        queue = get_sqs_queue()
        body = command.to_json()
        queue.send_message(MessageBody=body)
        logger.info(f"Sent PDFExportCommand to SQS for process {instance.id}")
    except Exception as e:
        logger.error(f"Failed to send PDFExportCommand to SQS for process {instance.id}: {e}", exc_info=True)
        instance.status = 'failed'
        instance.error_message = f"Failed to enqueue: {e}"
        instance.save(update_fields=['status', 'error_message', 'updated_at'])
