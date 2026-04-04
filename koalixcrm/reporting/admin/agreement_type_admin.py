# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import gettext as _


class AgreementTypeAdminView(admin.ModelAdmin):
    list_display = ('id',
                    'title',
                    'description')

    fieldsets = (
        (_('AgreementType'), {
            'fields': ('title',
                       'description')
        }),
    )
    save_as = True
