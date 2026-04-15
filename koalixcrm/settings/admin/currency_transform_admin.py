# -*- coding: utf-8 -*-
"""
CurrencyTransformInlineAdmin for koalixcrm settings
"""
from django.contrib import admin
from koalixcrm.settings.models.currency_transform import CurrencyTransform


class CurrencyTransformInlineAdmin(admin.TabularInline):
    model = CurrencyTransform
    extra = 1
    classes = ['collapse']
    fieldsets = (
        ('', {
            'fields': ('from_currency',
                       'to_currency',
                       'factor',)
        }),
    )
    allow_add = True
