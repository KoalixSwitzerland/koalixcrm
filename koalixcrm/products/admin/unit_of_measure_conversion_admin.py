# -*- coding: utf-8 -*-
"""UnitOfMeasureConversion admin for koalixcrm products (ADR-0005, REQ-0013)."""
from __future__ import annotations

from django.contrib import admin

from koalixcrm.core.admin.workspace_scoped_admin import WorkspaceScopedModelAdmin
from koalixcrm.products.models.unit_of_measure_conversion import (
    UnitOfMeasureConversion,
)


class UnitOfMeasureConversionInlineAdmin(admin.TabularInline):
    model = UnitOfMeasureConversion
    fk_name = "product"
    extra = 0
    classes = ['collapse']
    fields = ('from_unit', 'to_unit', 'factor')
    allow_add = True


@admin.register(UnitOfMeasureConversion)
class UnitOfMeasureConversionAdmin(WorkspaceScopedModelAdmin, admin.ModelAdmin):
    list_display = ('product', 'from_unit', 'to_unit', 'factor')
    list_filter = ('workspace',)
    search_fields = ('product__title',)
