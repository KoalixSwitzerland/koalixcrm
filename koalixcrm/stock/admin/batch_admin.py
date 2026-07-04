# -*- coding: utf-8 -*-
"""
BatchAdmin for koalixcrm stock
"""
from __future__ import annotations

from django.contrib import admin

from koalixcrm.core.admin.workspace_scoped_admin import WorkspaceScopedModelAdmin
from koalixcrm.stock.models.batch import Batch


@admin.register(Batch)
class BatchAdmin(WorkspaceScopedModelAdmin, admin.ModelAdmin):
    list_display = ('batch_number', 'variant', 'expiry_date', 'best_before_date', 'quarantine', 'received_at')
    list_filter = ('workspace', 'variant', 'quarantine')
    search_fields = ('batch_number', 'supplier_lot_number', 'variant__sku')
    autocomplete_fields = ('variant',)
    date_hierarchy = 'expiry_date'
