# -*- coding: utf-8 -*-
from __future__ import annotations

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.core.models.workspace_scoped import WorkspaceScopedModel


class PDFExportProcess(WorkspaceScopedModel):
    """
    Tracks the lifecycle of an asynchronous PDF generation job.

    Created by an admin action or programmatically. On creation, a Django signal
    sends a PDFExportCommand to the SQS queue, which is picked up by the Celery
    worker to execute the FOP-based PDF transformation.
    """

    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('processing', _('Processing')),
        ('completed', _('Completed')),
        ('failed', _('Failed')),
    ]

    id = models.BigAutoField(primary_key=True)

    source_model = models.CharField(
        verbose_name=_("Source Model"),
        max_length=100,
        help_text=_("Class name of the source object (e.g. Invoice, Quotation)")
    )
    source_id = models.BigIntegerField(
        verbose_name=_("Source Object ID"),
    )

    template_set = models.ForeignKey(
        "djangoUserExtension.DocumentTemplate",
        on_delete=models.SET_NULL,
        verbose_name=_("Template Set"),
        null=True,
        blank=True,
    )

    status = models.CharField(
        verbose_name=_("Status"),
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
    )

    # CharField, not URLField: the value is a machine-generated S3/MinIO URL,
    # never user input. Django's URLValidator requires a TLD or `localhost`, so
    # it rejects container-network hostnames like `http://minio:9000/...` and the
    # worker's status write-back fails with 400. Mirrors
    # `CommercialDocumentS3Media.s3_url`, which carries the same value.
    result_url = models.CharField(
        verbose_name=_("Result URL"),
        max_length=500,
        blank=True,
        default="",
        help_text=_("S3 URL of the generated PDF"),
    )

    error_message = models.TextField(
        verbose_name=_("Error Message"),
        blank=True,
        default="",
    )

    triggered_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name=_("Triggered By"),
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        verbose_name=_("Created At"),
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        verbose_name=_("Updated At"),
        auto_now=True,
    )

    class Meta:
        app_label = "core"
        db_table = "crm_pdfexportprocess"
        verbose_name = _("PDF Export Process")
        verbose_name_plural = _("PDF Export Processes")
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"PDFExport #{self.id} [{self.status}] {self.source_model}:{self.source_id}"
