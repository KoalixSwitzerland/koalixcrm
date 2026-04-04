# -*- coding: utf-8 -*-
"""
CurrencyAdmin for koalixcrm products
"""
from django.contrib import admin
from koalixcrm.products.models.currency import Currency


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'description',
                    'short_name',
                    'rounding')
    fieldsets = (('', {'fields': ('description',
                                  'short_name',
                                  'rounding')}),)
    allow_add = True
