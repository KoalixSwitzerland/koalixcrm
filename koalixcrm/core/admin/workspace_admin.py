# -*- coding: utf-8 -*-
"""
Admin registration for Workspace.

CR-8 §8.1.
"""
from __future__ import annotations

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from koalixcrm.core.models.workspace import Workspace


@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'color', 'date_added')
    search_fields = ('name', 'organization__party_ptr__matchcode')
    readonly_fields = ('date_added', 'last_modified')
    fieldsets = (
        (None, {
            'fields': ('name', 'organization', 'color'),
        }),
        (_('Timestamps'), {
            'fields': ('date_added', 'last_modified'),
            'classes': ('collapse',),
        }),
    )
