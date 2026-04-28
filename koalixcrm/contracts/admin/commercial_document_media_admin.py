# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Any

from django.contrib import admin

from koalixcrm.contracts.models.commercial_document_media import CommercialDocumentMedia
from koalixcrm.core.admin.workspace_scoped_admin import WorkspaceScopedModelAdmin


class CommercialDocumentMediaAdmin(WorkspaceScopedModelAdmin, admin.ModelAdmin):
    list_display = (
        'id',
        'commercial_document',
        'media_type',
        'status',
        'created_by',
        'created_at',
    )
    list_filter = ('workspace', 'status', 'media_type')
    readonly_fields = (
        's3_url',
        's3_key',
        'status',
        'pdf_export_process',
        'created_by',
        'created_at',
        'last_updated_at',
    )
    ordering = ('-created_at',)


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

    def has_add_permission(self, request: Any, obj: Any = None) -> bool:
        return False
