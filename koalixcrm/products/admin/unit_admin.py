# -*- coding: utf-8 -*-
"""
UnitAdmin for koalixcrm products
"""
from django.contrib import admin
from koalixcrm.products.models.unit import Unit


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'description',
                    'short_name',
                    'is_a_fraction_of',
                    'fraction_factor_to_next_higher_unit')
    fieldsets = (('', {'fields': ('description',
                                  'short_name',
                                  'is_a_fraction_of',
                                  'fraction_factor_to_next_higher_unit')}),)
    allow_add = True
