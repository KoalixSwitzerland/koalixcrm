# -*- coding: utf-8 -*-
from __future__ import annotations

from botocore.exceptions import ClientError
from django.conf import settings
from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext as _

from koalixcrm.contracts.models.commercial_document_media import CommercialDocumentMedia
from koalixcrm.core.admin.workspace_scoped_admin import WorkspaceScopedModelAdmin
from koalixcrm_utils.aws_clients import get_s3_client


def _extract_s3_key(source: str) -> str:
    if source.startswith('s3://'):
        # s3://bucket/key/path -> key/path
        return source.split('/', 3)[3]
    return source


class CommercialDocumentMediaAdmin(WorkspaceScopedModelAdmin, admin.ModelAdmin):
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
        's3_key',
        'status',
        'created_by',
        'created_at',
        'last_updated_at',
    )
    ordering = ('-created_at',)
    list_per_page = 20

    def download_link(self, obj):
        source = obj.s3_key or obj.s3_url
        if not source:
            return '-'
        try:
            s3_key = _extract_s3_key(source)
            filename = s3_key.split('/')[-1]
            expiry = getattr(settings, 'PRESIGNED_DOWNLOAD_URL_EXPIRY', 300)
            url = get_s3_client(use_presigned_config=True).generate_presigned_url(
                'get_object',
                Params={'Bucket': settings.S3_MEDIA_BUCKET, 'Key': s3_key},
                ExpiresIn=expiry,
            )
            return format_html('<a href="{}" target="_blank">{}</a>', url, filename)
        except ClientError as e:
            return f'Error: {str(e)}'

    download_link.short_description = _('File')


class CommercialDocumentMediaInline(admin.TabularInline):
    model = CommercialDocumentMedia
    extra = 0
    classes = ['collapse']
    readonly_fields = (
        's3_url',
        's3_key',
        'status',
        'media_type',
        'created_by',
        'created_at',
    )
    can_delete = False
    show_change_link = True

    def has_add_permission(self, request, obj=None):
        return False
