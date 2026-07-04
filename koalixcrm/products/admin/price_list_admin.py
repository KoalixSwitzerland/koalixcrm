# -*- coding: utf-8 -*-
"""PriceListAdmin for koalixcrm products (ADR-0005, REQ-0012)."""
from __future__ import annotations

from django.contrib import admin

from koalixcrm.core.admin.workspace_scoped_admin import WorkspaceScopedModelAdmin
from koalixcrm.products.admin.product_price_admin import (
    ProductPriceInlineForPriceList,
)
from koalixcrm.products.models.price_list import PriceList


@admin.register(PriceList)
class PriceListAdmin(WorkspaceScopedModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'channel', 'party_group')
    list_filter = ('workspace', 'channel')
    search_fields = ('name', 'channel')
    inlines = [ProductPriceInlineForPriceList]
