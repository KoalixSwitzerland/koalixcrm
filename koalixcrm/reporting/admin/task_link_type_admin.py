# -*- coding: utf-8 -*-
from __future__ import annotations

from django.contrib import admin
from django.utils.translation import gettext as _


class OptionTaskLinkType(admin.ModelAdmin):
    list_display = ('id',
                    'title',
                    'description')

    fieldsets = (
        (_('TaskLinkType'), {
            'fields': ('title',
                       'description')
        }),
    )
    save_as = True
