# -*- coding: utf-8 -*-
from __future__ import annotations

from django.contrib import admin
from django.utils.translation import gettext as _


class ResourceManagerAdminView(admin.ModelAdmin):
    list_display = ('id',
                    'user',)
    fieldsets = (
        (_('Basics'), {
            'fields': ('user',)
        }),
    )
