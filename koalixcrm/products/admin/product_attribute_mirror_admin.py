# -*- coding: utf-8 -*-
"""Read-only admin for `ProductAttributeMirror` — system-maintained via
signals (ADR-0004); shown for inspection, never editable."""
from __future__ import annotations

from django.contrib import admin

from koalixcrm.core.admin.workspace_scoped_admin import WorkspaceScopedModelAdmin
from koalixcrm.products.models.product_attribute_mirror import ProductAttributeMirror


@admin.register(ProductAttributeMirror)
class ProductAttributeMirrorAdmin(WorkspaceScopedModelAdmin, admin.ModelAdmin):
    list_display = ('product', 'variant', 'last_modification')
    list_filter = ('workspace',)
    search_fields = ('product__title',)
    readonly_fields = ('product', 'variant', 'data', 'last_modification')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
