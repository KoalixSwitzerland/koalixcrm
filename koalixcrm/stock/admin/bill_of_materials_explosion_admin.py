# -*- coding: utf-8 -*-
"""BillOfMaterialsExplosionAdmin for koalixcrm stock (ADR-0014). Read-only:
rows are only ever written by `services/bom_explosion.explode()`."""
from __future__ import annotations

from django.contrib import admin

from koalixcrm.core.admin.workspace_scoped_admin import WorkspaceScopedModelAdmin
from koalixcrm.stock.models.bill_of_materials_explosion import BillOfMaterialsExplosion


@admin.register(BillOfMaterialsExplosion)
class BillOfMaterialsExplosionAdmin(WorkspaceScopedModelAdmin, admin.ModelAdmin):
    list_display = ('bill_of_materials', 'bom_version', 'depth', 'bom_item', 'effective_qty', 'uom')
    list_filter = ('workspace', 'bill_of_materials')
    search_fields = ('bill_of_materials__product__title',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
