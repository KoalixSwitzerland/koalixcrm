# -*- coding: utf-8 -*-

from django.conf import settings
from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.core.models.s3_media import S3Media
from koalixcrm.core.models.workspace_scoped import WorkspaceScopedModel


class CommercialDocumentS3Media(S3Media, WorkspaceScopedModel):
    """
    S3-stored media file linked to a CommercialDocument.

    Extends the shared :class:`S3Media` base (ported from the Workflow Support
    Webapp), which supplies ``s3_url`` / ``status`` / ``media_type`` and the
    rule that ``s3_url`` holds a *relative object key*. Created by the PDF
    export worker after successful FOP transformation and S3 upload. Reused
    across all commercial document types (Invoice, Quotation, DespatchAdvice,
    PurchaseOrder, SalesOrder, PaymentReminder, CreditNote).
    """

    id = models.BigAutoField(primary_key=True)

    commercial_document = models.ForeignKey(
        "CommercialDocument",
        on_delete=models.CASCADE,
        verbose_name=_("Commercial Document"),
        related_name="media_files",
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

    def __str__(self) -> str:
        return (
            f"CommercialDocumentS3Media #{self.id} [{self.status}] "
            f"doc={self.commercial_document_id}"
        )
