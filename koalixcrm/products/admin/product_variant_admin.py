# -*- coding: utf-8 -*-
"""
ProductVariantInlineAdmin + ProductVariantAdmin for koalixcrm products
"""
from __future__ import annotations

from django.contrib import admin

from koalixcrm.core.admin.workspace_scoped_admin import WorkspaceScopedModelAdmin
from koalixcrm.products.admin.product_media_admin import ProductVariantMediaInlineAdmin
from koalixcrm.products.admin.product_price_admin import ProductPriceInlineAdmin
from koalixcrm.products.models.product_variant import ProductVariant


class ProductVariantInlineAdmin(admin.StackedInline):
    model = ProductVariant
    extra = 1
    classes = ['collapse']
    fields = (
        'sku',
        'gtin',
        'mpn',
        'weight_kg',
        ('dimensions_length_m', 'dimensions_width_m', 'dimensions_height_m'),
        'axis_values',
        'tracking_mode',
    )
    allow_add = True


@admin.register(ProductVariant)
class ProductVariantAdmin(WorkspaceScopedModelAdmin, admin.ModelAdmin):
    list_display = ('sku', 'product', 'gtin', 'mpn', 'weight_kg', 'tracking_mode')
    list_filter = ('workspace', 'tracking_mode')
    search_fields = ('sku', 'gtin', 'mpn')
    inlines = [ProductVariantMediaInlineAdmin, ProductPriceInlineAdmin]
