# -*- coding: utf-8 -*-
"""
ProductTranslationInlineAdmin for koalixcrm products
"""
from __future__ import annotations

from django.contrib import admin

from koalixcrm.products.models.product_translation import ProductTranslation


class ProductTranslationInlineAdmin(admin.TabularInline):
    model = ProductTranslation
    extra = 1
    classes = ['collapse']
    fields = ('language_code', 'name', 'short_description', 'long_description')
    allow_add = True
