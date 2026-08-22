# -*- coding: utf-8 -*-
from __future__ import annotations

from django.conf import settings
from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext as _

from koalixcrm.core.admin.s3_media_download import presigned_url_for_key, s3_key_from_url
from koalixcrm.core.models.pdf_export_process import PDFExportProcess


class PDFExportProcessAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'source_model',
        'source_id',
        'status',
        'result_link',
        'triggered_by',
        'created_at',
        'updated_at',
    )
    list_filter = ('status', 'source_model')
    readonly_fields = (
        'status',
        'result_url',
        'error_message',
        'created_at',
        'updated_at',
    )
    ordering = ('-created_at',)
    search_fields = ('source_model', 'source_id')

    @admin.display(description=_('Result'))
    def result_link(self, obj: PDFExportProcess) -> str:
        """Presigned download link for the finished PDF.

        `result_url` is written by the worker as an absolute, container-internal
        URL (`http://minio:9000/...`) that no browser can reach, so the object
        key is extracted and re-signed against the public endpoint.
        """
        if not obj.result_url:
            return '—'
        key = s3_key_from_url(obj.result_url, settings.S3_MEDIA_BUCKET)
        url = presigned_url_for_key(key) if key else ''
        if not url:
            return '—'
        return format_html(
            '<a href="{}" target="_blank" rel="noopener">{}</a>',
            url,
            key.rsplit('/', 1)[-1] or _('Open PDF'),
        )

    fieldsets = (
        (_('Export Request'), {
            'fields': (
                'source_model',
                'source_id',
                'template_set',
                'triggered_by',
            ),
        }),
        (_('Process Status'), {
            'fields': (
                'status',
                'result_url',
                'error_message',
                'created_at',
                'updated_at',
            ),
        }),
    )


admin.site.register(PDFExportProcess, PDFExportProcessAdmin)
