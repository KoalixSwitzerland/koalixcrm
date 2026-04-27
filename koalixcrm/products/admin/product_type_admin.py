# -*- coding: utf-8 -*-
"""
ProductTypeAdmin for koalixcrm products
"""
from django.contrib import admin
from django.utils.translation import gettext as _

from koalixcrm.core.admin.currency_transform_admin import CurrencyTransformInlineAdmin
from koalixcrm.core.admin.unit_transform_admin import UnitTransformInlineAdmin
from koalixcrm.core.admin.workspace_scoped_admin import WorkspaceScopedModelAdmin
from koalixcrm.products.admin.customer_group_transform_admin import (
    CustomerGroupTransformInlineAdmin,
)
from koalixcrm.products.admin.product_price_admin import ProductPriceInlineAdmin
from koalixcrm.products.models.product_type import ProductType


@admin.register(ProductType)
class ProductTypeAdmin(WorkspaceScopedModelAdmin, admin.ModelAdmin):
    list_display = (
        'product_type_identifier',
        'title',
        'default_unit',
        'tax')
    list_display_links = ('product_type_identifier',)
    list_filter = ('workspace',)
    fieldsets = (
        (_('Basics'), {
            'fields': (
                'product_type_identifier',
                'title',
                'description',
                'default_unit',
                'tax')
        }),
    )
    inlines = [ProductPriceInlineAdmin,
               UnitTransformInlineAdmin,
               CurrencyTransformInlineAdmin,
               CustomerGroupTransformInlineAdmin]
