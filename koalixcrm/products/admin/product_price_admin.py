# -*- coding: utf-8 -*-
"""
ProductPriceInlineAdmin for koalixcrm products
"""
from django.contrib import admin
from koalixcrm.products.models.product_price import ProductPrice


class ProductPriceInlineAdmin(admin.TabularInline):
    model = ProductPrice
    extra = 1
    classes = ['collapse']
    fieldsets = (
        ('', {
            'fields': ('price',
                       'currency',
                       'unit',
                       'valid_from',
                       'valid_until',
                       'party_group')
        }),
    )
    allow_add = True
