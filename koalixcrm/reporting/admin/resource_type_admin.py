# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import gettext as _


class ResourceTypeAdminView(admin.ModelAdmin):
    list_display = ('id',
                    'title',
                    'description')

    fieldsets = (
        (_('ResourceType'), {
            'fields': ('title',
                       'description')
        }),
    )
    save_as = True
