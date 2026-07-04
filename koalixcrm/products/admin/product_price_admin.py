# -*- coding: utf-8 -*-
"""
ProductPriceInlineAdmin for koalixcrm products.

ADR-0021 Amendment 2026-06-28: `ProductPrice` keys to `ProductVariant`, not
`Product` — `ProductPriceInlineAdmin` (fk_name='variant') is inlined on
`ProductVariantAdmin`. `ProductPriceInlineForPriceList` (fk_name='price_list')
is a second inline, on `PriceListAdmin`, grouping prices by channel/segment
(ADR-0005/REQ-0012).
"""
from __future__ import annotations

from django.contrib import admin
from django.utils.translation import gettext as _

from koalixcrm.core.admin.workspace_scoped_admin import WorkspaceScopedModelAdmin
from koalixcrm.products.models.product_price import ProductPrice


class ProductPriceInlineAdmin(admin.TabularInline):
    model = ProductPrice
    fk_name = "variant"
    extra = 1
    classes = ['collapse']
    fieldsets = (
        ('', {
            'fields': ('price',
                       'currency',
                       'unit',
                       'valid_from',
                       'valid_until',
                       'party_group',
                       'price_list')
        }),
    )
    allow_add = True


class ProductPriceInlineForPriceList(admin.TabularInline):
    model = ProductPrice
    fk_name = "price_list"
    extra = 0
    classes = ['collapse']
    fieldsets = (
        ('', {
            'fields': ('variant',
                       'price',
                       'currency',
                       'unit',
                       'valid_from',
                       'valid_until',
                       'party_group')
        }),
    )
    allow_add = True


@admin.register(ProductPrice)
class ProductPriceAdmin(WorkspaceScopedModelAdmin, admin.ModelAdmin):
    list_display = ('variant', 'price', 'currency', 'price_list', 'valid_from', 'valid_until', 'party_group')
    list_filter = ('workspace', 'price_list', 'currency')
    search_fields = ('variant__sku',)
