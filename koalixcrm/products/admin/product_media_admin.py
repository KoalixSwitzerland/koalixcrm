# -*- coding: utf-8 -*-
"""
ProductMediaInlineAdmin for koalixcrm products.

Registered twice: once inline on `Product` (product-level media) and once
inline on `ProductVariant` (variant-level media), reflecting the ADR-0021
"both levels" keying — the effective media pool of a variant is the union
of the two.
"""
from __future__ import annotations

from django.contrib import admin

from koalixcrm.core.admin.workspace_scoped_admin import WorkspaceScopedModelAdmin
from koalixcrm.products.models.product_media import ProductMedia


class ProductMediaInlineAdmin(admin.TabularInline):
    model = ProductMedia
    fk_name = "product"
    extra = 1
    classes = ['collapse']
    fields = ('media_type', 'object_key')
    allow_add = True


class ProductVariantMediaInlineAdmin(admin.TabularInline):
    model = ProductMedia
    fk_name = "variant"
    extra = 1
    classes = ['collapse']
    fields = ('media_type', 'object_key')
    allow_add = True


@admin.register(ProductMedia)
class ProductMediaAdmin(WorkspaceScopedModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'media_type', 'object_key', 'product', 'variant')
    list_filter = ('media_type', 'workspace')
    search_fields = ('object_key',)
