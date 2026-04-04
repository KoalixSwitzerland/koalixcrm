# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import gettext as _
from koalixcrm.plugin import *
from koalixcrm.contract_object_management.models.quote import Quote
from koalixcrm.contract_object_management.admin.sales_document_admin import OptionSalesDocument


class OptionQuote(OptionSalesDocument):
    list_display = OptionSalesDocument.list_display + ('valid_until',
                                                       'status',)
    list_filter = OptionSalesDocument.list_filter + ('status',)
    ordering = OptionSalesDocument.ordering
    search_fields = OptionSalesDocument.search_fields
    fieldsets = OptionSalesDocument.fieldsets + (
        (_('Quote specific'), {
            'fields': ('valid_until',
                       'status', )
        }),
    )

    save_as = OptionSalesDocument.save_as
    inlines = OptionSalesDocument.inlines

    actions = ['create_purchase_confirmation',
               'create_invoice',
               'create_quote',
               'create_delivery_note',
               'create_purchase_order',
               'create_project',
               'create_pdf']

    pluginProcessor = PluginProcessor()
    inlines.extend(pluginProcessor.getPluginAdditions("quoteInlines"))


class InlineQuote(admin.TabularInline):
    model = Quote
    classes = ['collapse']
    show_change_link = True
    can_delete = True
    extra = 1
    readonly_fields = ('link_to_quote',
                       'contract',
                       'customer',
                       'valid_until',
                       'status',
                       'last_pricing_date',
                       'last_calculated_price',
                       'last_calculated_tax',)
    fieldsets = (
        (_('Quote'), {
            'fields': ('link_to_quote',
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
