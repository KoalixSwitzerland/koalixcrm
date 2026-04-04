# -*- coding: utf-8 -*-
"""
UnitTransformInlineAdmin for koalixcrm products
"""
from django.contrib import admin
from koalixcrm.products.models.unit_transform import UnitTransform


class UnitTransformInlineAdmin(admin.TabularInline):
    model = UnitTransform
    extra = 1
    classes = ['collapse']
    fieldsets = (
        ('', {
            'fields': ('from_unit',
                       'to_unit',
                       'factor',)
        }),
    )
    allow_add = True
