# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import gettext as _

from koalixcrm.accounting.models.tax_account_assignment import TaxAccountAssignment


@admin.register(TaxAccountAssignment)
class TaxAccountAssignmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'tax', 'activa_account', 'passiva_account')
    list_display_links = ('id',)
    search_fields = ('tax__name',)
    fieldsets = (
        (_('Basics'), {
            'fields': ('tax', 'activa_account', 'passiva_account'),
        }),
    )


class TaxAccountAssignmentInline(admin.StackedInline):
    model = TaxAccountAssignment
    extra = 0
    max_num = 1
    can_delete = True
    fieldsets = (
        (_('Accounting'), {
            'fields': ('activa_account', 'passiva_account'),
        }),
    )
