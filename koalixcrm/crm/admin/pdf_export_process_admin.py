# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import gettext as _
from koalixcrm.crm.models.pdf_export_process import PDFExportProcess


class PDFExportProcessAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'source_model',
        'source_id',
        'status',
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
