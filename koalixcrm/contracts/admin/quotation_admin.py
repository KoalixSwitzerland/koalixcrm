# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import gettext as _
from koalixcrm.plugin import *  # noqa: F401, F403
from koalixcrm.contracts.models.quotation import Quotation
from koalixcrm.contracts.admin.commercial_document_admin import OptionCommercialDocument


class OptionQuotation(OptionCommercialDocument):
    list_display = OptionCommercialDocument.list_display + ('valid_until',
                                                       'status',)
    list_filter = OptionCommercialDocument.list_filter + ('status',)
    ordering = OptionCommercialDocument.ordering
    search_fields = OptionCommercialDocument.search_fields
    fieldsets = OptionCommercialDocument.fieldsets + (
        (_('Quotation specific'), {
            'fields': ('valid_until',
                       'status', )
        }),
    )

    save_as = OptionCommercialDocument.save_as
    inlines = OptionCommercialDocument.inlines

    actions = ['create_sales_order',
               'create_invoice',
               'create_quotation',
               'create_despatch_advice',
               'create_purchase_order',
               'create_project',
               'create_pdf_async']

    pluginProcessor = PluginProcessor()  # noqa: F405
    inlines.extend(pluginProcessor.getPluginAdditions("quotationInlines"))


class InlineQuotation(admin.TabularInline):
    model = Quotation
    classes = ['collapse']
    show_change_link = True
    can_delete = True
    extra = 1
    readonly_fields = ('link_to_quotation',
                       'contract',
                       'customer',
                       'valid_until',
                       'status',
                       'last_pricing_date',
                       'last_calculated_price',
                       'last_calculated_tax',)
    fieldsets = (
        (_('Quotation'), {
            'fields': ('link_to_quotation',
                       'contract',
                       'customer',
                       'valid_until',
                       'status',
                       'last_pricing_date',
                       'last_calculated_price',
                       'last_calculated_tax',)
        }),
    )
    allow_add = False
