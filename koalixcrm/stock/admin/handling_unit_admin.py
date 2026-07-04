# -*- coding: utf-8 -*-
"""
HandlingUnitAdmin for koalixcrm stock
"""
from __future__ import annotations

from django.contrib import admin

from koalixcrm.core.admin.workspace_scoped_admin import WorkspaceScopedModelAdmin
from koalixcrm.stock.models.handling_unit import HandlingUnit


@admin.register(HandlingUnit)
class HandlingUnitAdmin(WorkspaceScopedModelAdmin, admin.ModelAdmin):
    list_display = ('sscc', 'hu_type', 'location', 'parent_handling_unit', 'is_open')
    list_filter = ('workspace', 'hu_type', 'is_open', 'location')
    search_fields = ('sscc', 'location__code', 'location__name')
    autocomplete_fields = ('parent_handling_unit', 'location')
