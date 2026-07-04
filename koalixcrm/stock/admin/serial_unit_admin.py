# -*- coding: utf-8 -*-
"""
SerialUnitAdmin for koalixcrm stock
"""
from __future__ import annotations

from django.contrib import admin

from koalixcrm.core.admin.workspace_scoped_admin import WorkspaceScopedModelAdmin
from koalixcrm.stock.models.serial_unit import SerialUnit


@admin.register(SerialUnit)
class SerialUnitAdmin(WorkspaceScopedModelAdmin, admin.ModelAdmin):
    list_display = ('serial_number', 'variant', 'condition_state', 'batch', 'decommissioned_at')
    list_filter = ('workspace', 'variant', 'condition_state')
    search_fields = ('serial_number', 'global_uid', 'variant__sku')
    autocomplete_fields = ('variant', 'batch')
    readonly_fields = ('decommissioned_at',)

    def has_delete_permission(self, request, obj=None):
        # ADR-0012: soft-delete-forever. SerialUnit.delete() already refuses
        # unless decommissioned + retention floor elapsed; hide the admin
        # delete action entirely to avoid a misleading "delete succeeded"
        # UX for the common (not-yet-eligible) case.
        return False
