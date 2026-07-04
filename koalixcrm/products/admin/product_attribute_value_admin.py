# -*- coding: utf-8 -*-
"""Admin for the six typed EAV value tables (ADR-0004). Each gets its own
list admin (bulk maintenance / search) plus a `TabularInline` usable from
`ProductAdmin`/`ProductVariantAdmin` so attribute-value maintenance is
workable directly on the product edit page, per ADR-0002's "Django admin
is a first-class UI" stance."""
from __future__ import annotations

from django.contrib import admin

from koalixcrm.core.admin.workspace_scoped_admin import WorkspaceScopedModelAdmin
from koalixcrm.products.models.product_attribute_bool import ProductAttributeBool
from koalixcrm.products.models.product_attribute_decimal import ProductAttributeDecimal
from koalixcrm.products.models.product_attribute_enum import ProductAttributeEnum
from koalixcrm.products.models.product_attribute_int import ProductAttributeInt
from koalixcrm.products.models.product_attribute_reference import (
    ProductAttributeReference,
)
from koalixcrm.products.models.product_attribute_string import ProductAttributeString


class ProductAttributeStringInlineAdmin(admin.TabularInline):
    model = ProductAttributeString
    extra = 0
    fields = ('variant', 'attribute_definition', 'value')


class ProductAttributeIntInlineAdmin(admin.TabularInline):
    model = ProductAttributeInt
    extra = 0
    fields = ('variant', 'attribute_definition', 'value')


class ProductAttributeDecimalInlineAdmin(admin.TabularInline):
    model = ProductAttributeDecimal
    extra = 0
    fields = ('variant', 'attribute_definition', 'value', 'unit')


class ProductAttributeBoolInlineAdmin(admin.TabularInline):
    model = ProductAttributeBool
    extra = 0
    fields = ('variant', 'attribute_definition', 'value')


class ProductAttributeEnumInlineAdmin(admin.TabularInline):
    model = ProductAttributeEnum
    extra = 0
    fields = ('variant', 'attribute_definition', 'value')


class ProductAttributeReferenceInlineAdmin(admin.TabularInline):
    model = ProductAttributeReference
    extra = 0
    fields = ('variant', 'attribute_definition', 'content_type', 'object_id')


@admin.register(ProductAttributeString)
class ProductAttributeStringAdmin(WorkspaceScopedModelAdmin, admin.ModelAdmin):
    list_display = ('product', 'variant', 'attribute_definition', 'value')
    list_filter = ('workspace', 'attribute_definition')
    search_fields = ('product__title', 'attribute_definition__key')


@admin.register(ProductAttributeInt)
class ProductAttributeIntAdmin(WorkspaceScopedModelAdmin, admin.ModelAdmin):
    list_display = ('product', 'variant', 'attribute_definition', 'value')
    list_filter = ('workspace', 'attribute_definition')
    search_fields = ('product__title', 'attribute_definition__key')


@admin.register(ProductAttributeDecimal)
class ProductAttributeDecimalAdmin(WorkspaceScopedModelAdmin, admin.ModelAdmin):
    list_display = ('product', 'variant', 'attribute_definition', 'value', 'unit')
    list_filter = ('workspace', 'attribute_definition')
    search_fields = ('product__title', 'attribute_definition__key')


@admin.register(ProductAttributeBool)
class ProductAttributeBoolAdmin(WorkspaceScopedModelAdmin, admin.ModelAdmin):
    list_display = ('product', 'variant', 'attribute_definition', 'value')
    list_filter = ('workspace', 'attribute_definition')
    search_fields = ('product__title', 'attribute_definition__key')


@admin.register(ProductAttributeEnum)
class ProductAttributeEnumAdmin(WorkspaceScopedModelAdmin, admin.ModelAdmin):
    list_display = ('product', 'variant', 'attribute_definition', 'value')
    list_filter = ('workspace', 'attribute_definition')
    search_fields = ('product__title', 'attribute_definition__key')


@admin.register(ProductAttributeReference)
class ProductAttributeReferenceAdmin(WorkspaceScopedModelAdmin, admin.ModelAdmin):
    list_display = ('product', 'variant', 'attribute_definition', 'content_type', 'object_id')
    list_filter = ('workspace', 'attribute_definition', 'content_type')
    search_fields = ('product__title', 'attribute_definition__key')
