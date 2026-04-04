# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import gettext as _


class EstimationStatusAdminView(admin.ModelAdmin):
    list_display = ('id',
                    'title',
                    'description',
                    'is_obsolete')

    fieldsets = (
        (_('Agreement Status'), {
            'fields': ('title',
                       'description',
                       'is_obsolete')
        }),
    )
    save_as = True
