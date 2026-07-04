# -*- coding: utf-8 -*-
"""ProductPassport admin for koalixcrm products (ADR-0008)."""
from __future__ import annotations

from django.contrib import admin

from koalixcrm.core.admin.workspace_scoped_admin import WorkspaceScopedModelAdmin
from koalixcrm.products.models.product_passport import ProductPassport


class ProductPassportInlineAdmin(admin.StackedInline):
    model = ProductPassport
    fk_name = "product"
    extra = 0
    max_num = 1
    classes = ['collapse']
    fields = ('passport_data',)
    allow_add = True


@admin.register(ProductPassport)
class ProductPassportAdmin(WorkspaceScopedModelAdmin, admin.ModelAdmin):
    list_display = ('product',)
    list_filter = ('workspace',)
    search_fields = ('product__title',)
