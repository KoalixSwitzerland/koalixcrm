# -*- coding: utf-8 -*-
"""
CustomerGroupTransformInlineAdmin for koalixcrm products
"""
from django.contrib import admin
from koalixcrm.products.models.customer_group_transform import CustomerGroupTransform


class CustomerGroupTransformInlineAdmin(admin.TabularInline):
    model = CustomerGroupTransform
    extra = 1
    classes = ['collapse']
    fieldsets = (
        ('', {
            'fields': ('from_customer_group',
                       'to_customer_group',
                       'factor',)
        }),
    )
    allow_add = True
