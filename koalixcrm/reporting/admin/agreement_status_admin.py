# -*- coding: utf-8 -*-
from __future__ import annotations

from django.contrib import admin
from django.utils.translation import gettext as _


class AgreementStatusAdminView(admin.ModelAdmin):
    list_display = ('id',
                    'title',
                    'description',
                    'is_agreed')

    fieldsets = (
        (_('Agreement Status'), {
            'fields': ('title',
                       'description',
                       'is_agreed')
        }),
    )
    save_as = True
