# -*- coding: utf-8 -*-
"""BillOfMaterials + BomItem admin for koalixcrm products (ADR-0006, REQ-0015)."""
from __future__ import annotations

from django.contrib import admin

from koalixcrm.core.admin.workspace_scoped_admin import WorkspaceScopedModelAdmin
from koalixcrm.products.models.bill_of_materials import BillOfMaterials
from koalixcrm.products.models.bom_item import BomItem


class BomItemInlineAdmin(admin.TabularInline):
    model = BomItem
    fk_name = "bill_of_materials"
    extra = 1
    classes = ['collapse']
    fields = ('component_product', 'quantity', 'unit', 'scrap_pct', 'alternative_component',
              'default_component_variant')
    allow_add = True


class BillOfMaterialsInlineAdmin(admin.StackedInline):
    model = BillOfMaterials
    fk_name = "product"
    extra = 0
    max_num = 1
    classes = ['collapse']
    fields = ('name', 'description')
    allow_add = True


@admin.register(BillOfMaterials)
class BillOfMaterialsAdmin(WorkspaceScopedModelAdmin, admin.ModelAdmin):
    list_display = ('product', 'name')
    list_filter = ('workspace',)
    search_fields = ('product__title', 'name')
    inlines = [BomItemInlineAdmin]


@admin.register(BomItem)
class BomItemAdmin(WorkspaceScopedModelAdmin, admin.ModelAdmin):
    list_display = ('bill_of_materials', 'component_product', 'quantity', 'unit', 'scrap_pct')
    list_filter = ('workspace',)
    search_fields = ('bill_of_materials__product__title', 'component_product__title')
