# -*- coding: utf-8 -*-
"""
TaxAdmin for koalixcrm products
"""
from django.contrib import admin
from koalixcrm.products.models.tax import Tax


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'tax_rate',
                    'name',
                    'account_activa',
                    'account_passiva')
    fieldsets = (('', {'fields': ('tax_rate',
                                  'name',
                                  'account_activa',
                                  'account_passiva')}),)
    allow_add = True
