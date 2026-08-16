# -*- coding: utf-8 -*-
"""Admin for `AttributeDefinition` (ADR-0004). Hybrid scope — see
`AttributeGroupAdmin` docstring."""
from __future__ import annotations

from django.contrib import admin

from koalixcrm.products.models.attribute_definition import AttributeDefinition


@admin.register(AttributeDefinition)
class AttributeDefinitionAdmin(admin.ModelAdmin):
    list_display = (
        'key', 'canonical_key', 'label', 'data_type', 'scope', 'workspace',
        'group', 'is_required', 'is_multivalued',
    )
    list_filter = ('scope', 'data_type', 'workspace', 'group')
    search_fields = ('key', 'canonical_key', 'label')
    fieldsets = (
        (None, {'fields': ('workspace', 'scope', 'key', 'canonical_key', 'label', 'group', 'order')}),
        ('Data Type', {'fields': ('data_type', 'unit', 'enum_values')}),
        ('Validation', {'fields': ('min_value', 'max_value', 'regex', 'is_required', 'is_multivalued', 'is_localized')}),
    )
