# -*- coding: utf-8 -*-
"""
CurrencyAdmin for koalixcrm settings
"""
from __future__ import annotations

from django.contrib import admin

from koalixcrm.core.models.currency import Currency


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
