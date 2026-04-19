# -*- coding: utf-8 -*-
"""
Admin registration for RoleInWorkspace.

CR-8 §8.3.
"""

from django.contrib import admin

from koalixcrm.core.models.access import RoleInWorkspace


@admin.register(RoleInWorkspace)
class RoleInWorkspaceAdmin(admin.ModelAdmin):
    list_display = ('group', 'workspace', 'role')
    list_filter = ('workspace', 'role')
    search_fields = ('group__name', 'workspace__name')
    raw_id_fields = ('group',)
