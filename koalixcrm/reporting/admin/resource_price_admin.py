# -*- coding: utf-8 -*-
from __future__ import annotations

from django.contrib import admin

from koalixcrm.reporting.models.resource_price import ResourcePrice


class ResourcePriceInlineAdminView(admin.TabularInline):
    model = ResourcePrice
    extra = 1
    classes = ['collapse']
    fieldsets = (
        ('Basic', {
            'fields': ('price',
                       'currency',
                       'unit',
                       'valid_from',
                       'valid_until',
                       'customer_group')
        }),
    )
    allow_add = True
