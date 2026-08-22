# -*- coding: utf-8 -*-
from __future__ import annotations

from django.contrib import admin

from koalixcrm.contracts.models.commercial_document_media import CommercialDocumentS3Media
from koalixcrm.core.admin.s3_media_download import S3MediaDownloadMixin
from koalixcrm.core.admin.workspace_scoped_admin import WorkspaceScopedModelAdmin


class CommercialDocumentS3MediaAdmin(
    S3MediaDownloadMixin,
    WorkspaceScopedModelAdmin,
    admin.ModelAdmin,
):
    list_display = (
        'id',
        'commercial_document',
        'media_type',
        'status',
        'download_link',
        'created_by',
        'created_at',
    )
    list_filter = ('workspace', 'status', 'media_type')
    readonly_fields = (
        's3_url',
        'download_link',
        'status',
        'created_by',
        'created_at',
        'last_updated_at',
    )
    ordering = ('-created_at',)
    list_per_page = 20


class CommercialDocumentS3MediaInline(S3MediaDownloadMixin, admin.TabularInline):
    """Read-only inline listing the PDFs generated for a commercial document.

    Shown on Invoice / Quotation / SalesOrder / … change pages. Rows are
    created by the PDF export worker, never by hand, so adding and deleting
    are both disabled.
    """

    model = CommercialDocumentS3Media
    extra = 0
    classes = ['collapse']
    fields = (
        'download_link',
        's3_url',
        'status',
        'media_type',
        'created_by',
        'created_at',
    )
    readonly_fields = fields
    can_delete = False
    show_change_link = True

    def has_add_permission(self, request, obj=None) -> bool:
        return False
