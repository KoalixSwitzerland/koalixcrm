# -*- coding: utf-8 -*-
"""Admin for `AttributeGroup` (ADR-0004). Hybrid scope (global/workspace) —
no `WorkspaceScopedModelAdmin` mixin, since a superuser or platform admin
must be able to create GLOBAL-scope (workspace=None) rows here."""
from __future__ import annotations

from django.contrib import admin

from koalixcrm.products.models.attribute_group import AttributeGroup


@admin.register(AttributeGroup)
class AttributeGroupAdmin(admin.ModelAdmin):
    list_display = ('key', 'name', 'scope', 'workspace')
    list_filter = ('scope', 'workspace')
    search_fields = ('key', 'name')
