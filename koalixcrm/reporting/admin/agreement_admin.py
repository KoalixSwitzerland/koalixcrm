# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import gettext as _

from koalixcrm.reporting.models.agreement import Agreement


class AgreementInlineAdminView(admin.TabularInline):
    model = Agreement
    fieldsets = (
        (_('Work'), {
            'fields': ('task',
                       'resource',
                       'amount',
                       'unit',
                       'costs',
                       'date_from',
                       'date_until',
                       'type',
                       'status')
        }),
    )
    extra = 1
