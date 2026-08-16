# -*- coding: utf-8 -*-
"""
ProductFamilyAdmin for koalixcrm products
"""
from __future__ import annotations

from django.contrib import admin

from koalixcrm.core.admin.workspace_scoped_admin import WorkspaceScopedModelAdmin
from koalixcrm.products.models.product_family import ProductFamily


@admin.register(ProductFamily)
class ProductFamilyAdmin(WorkspaceScopedModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'name')
    list_filter = ('workspace',)
    search_fields = ('name',)
