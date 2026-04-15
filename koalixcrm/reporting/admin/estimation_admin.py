# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import gettext as _
from koalixcrm.reporting.models.estimation import Estimation, EstimationAdminForm


class EstimationInlineAdminView(admin.TabularInline):
    model = Estimation
    formset = EstimationAdminForm
    fieldsets = (
        (_('Work'), {
            'fields': ('task',
                       'amount',
                       'resource',
                       'date_from',
                       'date_until',
                       'status',
                       'reporting_period')
        }),
    )
    extra = 1
