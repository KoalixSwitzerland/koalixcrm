# -*- coding: utf-8 -*-
"""Admin for the global classification taxonomy (ADR-0004)."""
from __future__ import annotations

from django.contrib import admin

from koalixcrm.products.models.classification import Classification, ClassificationNode


@admin.register(Classification)
class ClassificationAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'description')
    search_fields = ('code', 'name')


@admin.register(ClassificationNode)
class ClassificationNodeAdmin(admin.ModelAdmin):
    list_display = ('classification', 'code', 'name', 'parent', 'level')
    list_filter = ('classification', 'level')
    search_fields = ('code', 'name')
    autocomplete_fields = ('parent',)
