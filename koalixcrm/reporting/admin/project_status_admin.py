# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import gettext as _


class OptionProjectStatus(admin.ModelAdmin):
    list_display = ('id',
                    'title',
                    'description',
                    'is_done')

    fieldsets = (
        (_('Project Status'), {
            'fields': ('title',
                       'description',
                       'is_done')
        }),
    )
    save_as = True
