# -*- coding: utf-8 -*-
from __future__ import annotations

from django.contrib import admin
from django.utils.translation import gettext as _

from koalixcrm.core.admin.workspace_scoped_admin import WorkspaceScopedModelAdmin


class ResourceManagerAdminView(WorkspaceScopedModelAdmin, admin.ModelAdmin):
    list_display = ('id',
                    'user',)
    fieldsets = (
        (_('Basics'), {
            'fields': ('user',)
        }),
    )
