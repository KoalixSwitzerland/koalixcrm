# -*- coding: utf-8 -*-
"""
OnHandRecordAdmin for koalixcrm stock. `OnHandRecord` is a granular, stored
projection row that is only ever authorized to change via
`services/movement_posting.py` (ADR-0011: "direct `StockMovement.objects
.create(...)` calls bypass that and must not be used outside the
service" applies equally to the projections it maintains). The admin is
therefore a read-only view, exactly like `StockBalanceAdmin` — add/change/
delete are all refused so the movement log stays the single write path.
"""
from __future__ import annotations

from django.contrib import admin

from koalixcrm.core.admin.workspace_scoped_admin import WorkspaceScopedModelAdmin
from koalixcrm.stock.models.on_hand_record import OnHandRecord


@admin.register(OnHandRecord)
class OnHandRecordAdmin(WorkspaceScopedModelAdmin, admin.ModelAdmin):
    list_display = ('variant', 'location', 'qty_on_hand', 'uom', 'owner_type', 'owner_party',
                     'batch', 'serial_unit', 'handling_unit')
    list_filter = ('workspace', 'owner_type', 'location', 'variant')
    search_fields = ('variant__sku', 'location__code', 'batch__batch_number', 'serial_unit__serial_number')
    autocomplete_fields = ('variant', 'location', 'batch', 'serial_unit', 'handling_unit', 'owner_party')
    readonly_fields = [f.name for f in OnHandRecord._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
