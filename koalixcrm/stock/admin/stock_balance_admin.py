# -*- coding: utf-8 -*-
"""StockBalanceAdmin for koalixcrm stock (ADR-0010). Read-only projection:
creation/updates happen exclusively via services/movement_posting.py and
services/reservation_lifecycle.py."""
from __future__ import annotations

from django.contrib import admin

from koalixcrm.core.admin.workspace_scoped_admin import WorkspaceScopedModelAdmin
from koalixcrm.stock.models.stock_balance import StockBalance


@admin.register(StockBalance)
class StockBalanceAdmin(WorkspaceScopedModelAdmin, admin.ModelAdmin):
    list_display = ('variant', 'location', 'qty_on_hand', 'qty_booked',
                     'qty_reserved_for_document', 'qty_ordered', 'qty_in_transit',
                     'qty_quarantine', 'atp', 'uom')
    list_filter = ('workspace', 'location')
    search_fields = ('variant__sku', 'location__code')
    readonly_fields = [f.name for f in StockBalance._meta.fields] + ['atp']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def atp(self, obj):
        return obj.atp
