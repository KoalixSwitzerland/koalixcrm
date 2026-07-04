# -*- coding: utf-8 -*-
"""MovementReasonCodeAdmin for koalixcrm stock. Global lookup table."""
from __future__ import annotations

from django.contrib import admin

from koalixcrm.stock.models.movement_reason_code import MovementReasonCode
from koalixcrm.stock.models.movement_reason_code_extension import MovementReasonCodeExtension
from koalixcrm.core.admin.workspace_scoped_admin import WorkspaceScopedModelAdmin


@admin.register(MovementReasonCode)
class MovementReasonCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'label_en', 'label_de')
    search_fields = ('code', 'label_en', 'label_de')


@admin.register(MovementReasonCodeExtension)
class MovementReasonCodeExtensionAdmin(WorkspaceScopedModelAdmin, admin.ModelAdmin):
    list_display = ('code', 'label_en', 'label_de', 'workspace')
    list_filter = ('workspace',)
    search_fields = ('code', 'label_en', 'label_de')
