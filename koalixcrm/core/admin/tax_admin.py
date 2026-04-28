# -*- coding: utf-8 -*-
"""
TaxAdmin for koalixcrm settings
"""
from __future__ import annotations

from django.contrib import admin

from koalixcrm.core.models.tax import Tax


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'tax_rate',
                    'name')
    fieldsets = (('', {'fields': ('tax_rate',
                                  'name')}),)
    allow_add = True
