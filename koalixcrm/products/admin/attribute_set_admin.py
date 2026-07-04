# -*- coding: utf-8 -*-
"""Admin for `AttributeSet` and its bound groups/defaults/validation rules
(ADR-0004, ADR-0020). This is the main UI surface for configuring an
industry attribute template: bind groups, set per-attribute defaults, and
declare cross-field validation rules — all without a code deploy."""
from __future__ import annotations

from django.contrib import admin

from koalixcrm.core.admin.workspace_scoped_admin import WorkspaceScopedModelAdmin
from koalixcrm.products.models.attribute_set import AttributeSet, AttributeSetGroup
from koalixcrm.products.models.attribute_set_default import AttributeSetDefault
from koalixcrm.products.models.attribute_validation_rule import AttributeValidationRule


class AttributeSetGroupInlineAdmin(admin.TabularInline):
    model = AttributeSetGroup
    extra = 1
    fields = ('attribute_group', 'order')


class AttributeSetDefaultInlineAdmin(admin.TabularInline):
    model = AttributeSetDefault
    extra = 0
    fields = ('attribute_definition', 'default_value')


class AttributeValidationRuleInlineAdmin(admin.TabularInline):
    model = AttributeValidationRule
    extra = 0
    fields = ('key', 'name', 'order', 'is_active', 'condition', 'then')


@admin.register(AttributeSet)
class AttributeSetAdmin(WorkspaceScopedModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'classification_node', 'kind', 'product_family', 'workspace')
    list_filter = ('workspace', 'kind', 'classification_node')
    search_fields = ('name',)
    inlines = [AttributeSetGroupInlineAdmin, AttributeSetDefaultInlineAdmin, AttributeValidationRuleInlineAdmin]


@admin.register(AttributeValidationRule)
class AttributeValidationRuleAdmin(WorkspaceScopedModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'attribute_set', 'order', 'is_active')
    list_filter = ('workspace', 'is_active', 'attribute_set')
    search_fields = ('key', 'name')
