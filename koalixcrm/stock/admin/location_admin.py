# -*- coding: utf-8 -*-
"""
LocationAdmin for koalixcrm stock — makes the n-level hierarchy navigable
via a parent filter/search and a breadcrumb display (REQ-0018).
"""
from __future__ import annotations

from django.contrib import admin

from koalixcrm.core.admin.workspace_scoped_admin import WorkspaceScopedModelAdmin
from koalixcrm.stock.models.location import Location


@admin.register(Location)
class LocationAdmin(WorkspaceScopedModelAdmin, admin.ModelAdmin):
    list_display = ('code', 'name', 'location_type', 'breadcrumb', 'parent', 'is_active', 'external_ref')
    list_display_links = ('code', 'name')
    list_filter = ('workspace', 'location_type', 'is_active', 'parent')
    search_fields = ('code', 'name', 'external_ref', 'parent__code', 'parent__name')
    autocomplete_fields = ('parent',)

    def breadcrumb(self, obj: Location) -> str:
        return " / ".join(loc.code for loc in obj.get_ancestor_path())
    breadcrumb.short_description = "Path"
