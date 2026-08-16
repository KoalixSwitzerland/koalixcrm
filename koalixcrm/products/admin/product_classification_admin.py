# -*- coding: utf-8 -*-
from __future__ import annotations

from django.contrib import admin

from koalixcrm.core.admin.workspace_scoped_admin import WorkspaceScopedModelAdmin
from koalixcrm.products.models.product_classification import ProductClassification


class ProductClassificationInlineAdmin(admin.TabularInline):
    model = ProductClassification
    extra = 0
    fields = ('classification_node',)
    autocomplete_fields = ('classification_node',)


@admin.register(ProductClassification)
class ProductClassificationAdmin(WorkspaceScopedModelAdmin, admin.ModelAdmin):
    list_display = ('product', 'classification_node', 'date_of_creation')
    list_filter = ('workspace',)
    search_fields = ('product__title', 'classification_node__name', 'classification_node__code')
