# -*- coding: utf-8 -*-
from __future__ import annotations

from django.contrib import admin

from koalixcrm.core.admin.workspace_scoped_admin import WorkspaceScopedModelAdmin
from koalixcrm.products.models.product_attribute_mapping import ProductAttributeMapping


@admin.register(ProductAttributeMapping)
class ProductAttributeMappingAdmin(WorkspaceScopedModelAdmin, admin.ModelAdmin):
    list_display = ('source_standard', 'source_attribute_id', 'canonical_key', 'workspace')
    list_filter = ('workspace', 'source_standard')
    search_fields = ('source_attribute_id', 'canonical_key')
