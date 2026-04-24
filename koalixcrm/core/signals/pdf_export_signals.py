"""
Signal for PDFExportProcess: on creation, dispatch a PDFExportCommand via
the configured dispatcher (see CR-4 / KOALIXCRM_PDF_EXPORT_DISPATCHER).
"""
import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from koalixcrm.core.models.pdf_export_process import PDFExportProcess
from koalixcrm_mq_commands import PDFExportCommand

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
        from koalixcrm.core.pdf_export_dispatch import get_dispatcher
        dispatcher = get_dispatcher()
        dispatcher(command)
        logger.info(f"Dispatched PDFExportCommand for process {instance.id}")
    except Exception as e:
        logger.error(f"Failed to dispatch PDFExportCommand for process {instance.id}: {e}", exc_info=True)
        instance.status = 'failed'
        instance.error_message = f"Failed to enqueue: {e}"
        instance.save(update_fields=['status', 'error_message', 'updated_at'])
