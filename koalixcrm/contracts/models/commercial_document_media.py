# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.utils.translation import gettext as _


class CommercialDocumentMedia(models.Model):
    """
    S3-stored media file linked to a CommercialDocument.

    Follows the S3Media pattern (see qq_workflow_support.models.s3_media).
    Created by the Celery PDF export task after successful FOP transformation
    and S3 upload.  Reused across all commercial document types (Invoice, Quotation,
    DespatchAdvice, PurchaseOrder, SalesOrder, PaymentReminder).
    """

    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('processing', _('Processing')),
        ('completed', _('Completed')),
        ('failed', _('Failed')),
    ]

    id = models.BigAutoField(primary_key=True)

    commercial_document = models.ForeignKey(
        "CommercialDocument",
        on_delete=models.CASCADE,
        verbose_name=_("Commercial Document"),
        related_name="media_files",
    )

    s3_url = models.CharField(
        verbose_name=_("S3 URL"),
        max_length=500,
        help_text=_("Full URL to the file in S3 / MinIO"),
    )

    s3_key = models.CharField(
        verbose_name=_("S3 Key"),
        max_length=500,
        blank=True,
        default="",
        help_text=_("Object key inside the S3 bucket"),
    )

    status = models.CharField(
        verbose_name=_("Status"),
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
    )

    media_type = models.CharField(
        verbose_name=_("Media Type"),
        max_length=50,
        default='application/pdf',
        help_text=_("MIME type of the stored file"),
    )

    pdf_export_process = models.ForeignKey(
        "core.PDFExportProcess",
        on_delete=models.SET_NULL,
        verbose_name=_("PDF Export Process"),
        related_name="media_files",
        null=True,
        blank=True,
        help_text=_("The async export process that created this media"),
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name=_("Created By"),
        related_name="created_commercial_document_media",
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        verbose_name=_("Created At"),
        auto_now_add=True,
        db_index=True,
    )

    last_updated_at = models.DateTimeField(
        verbose_name=_("Last Updated At"),
        auto_now=True,
    )

    class Meta:
        app_label = "contract_object_management"
        db_table = "crm_commercialdocumentmedia"
        verbose_name = _("Commercial Document Media")
        verbose_name_plural = _("Commercial Document Media")
        ordering = ['-created_at']

    def __str__(self):
        return f"CommercialDocumentMedia #{self.id} [{self.status}] doc={self.commercial_document_id}"
