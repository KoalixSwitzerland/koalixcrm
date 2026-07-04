# -*- coding: utf-8 -*-
"""ProductSupply admin for koalixcrm products (ADR-0006, REQ-0014)."""
from __future__ import annotations

from django.contrib import admin

from koalixcrm.core.admin.workspace_scoped_admin import WorkspaceScopedModelAdmin
from koalixcrm.products.models.product_supply import ProductSupply


class ProductSupplyInlineAdmin(admin.TabularInline):
    model = ProductSupply
    fk_name = "product"
    extra = 0
    classes = ['collapse']
    fields = ('supplier', 'supplier_sku', 'lead_time_days', 'moq', 'purchase_price', 'purchase_currency')
    allow_add = True


@admin.register(ProductSupply)
class ProductSupplyAdmin(WorkspaceScopedModelAdmin, admin.ModelAdmin):
    list_display = ('product', 'supplier', 'supplier_sku', 'lead_time_days', 'moq', 'purchase_price')
    list_filter = ('workspace',)
    search_fields = ('product__title', 'supplier__display_name', 'supplier_sku')
