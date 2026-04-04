# -*- coding: utf-8 -*-
"""
ProductTypeAdmin for koalixcrm products
"""
from django.contrib import admin
from django.utils.translation import gettext as _
from koalixcrm.products.models.product_type import ProductType
from koalixcrm.products.admin.product_price_admin import ProductPriceInlineAdmin
from koalixcrm.products.admin.unit_transform_admin import UnitTransformInlineAdmin
from koalixcrm.products.admin.currency_transform_admin import CurrencyTransformInlineAdmin
from koalixcrm.products.admin.customer_group_transform_admin import CustomerGroupTransformInlineAdmin


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = (
        'product_type_identifier',
        'title',
        'default_unit',
        'tax',
        'accounting_product_category')
    list_display_links = ('product_type_identifier',)
    fieldsets = (
        (_('Basics'), {
            'fields': (
                'product_type_identifier',
                'title',
                'description',
                'default_unit',
                'tax',
                'accounting_product_category')
        }),
    )
    inlines = [ProductPriceInlineAdmin,
               UnitTransformInlineAdmin,
               CurrencyTransformInlineAdmin,
               CustomerGroupTransformInlineAdmin]
