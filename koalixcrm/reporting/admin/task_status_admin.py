# -*- coding: utf-8 -*-
from __future__ import annotations

from django.contrib import admin
from django.utils.translation import gettext as _


class OptionTaskStatus(admin.ModelAdmin):
    list_display = ('id',
                    'title',
                    'description',
                    'is_done')

    fieldsets = (
        (_('Task Status'), {
            'fields': ('title',
                       'description',
                       'is_done')
        }),
    )
    save_as = True
