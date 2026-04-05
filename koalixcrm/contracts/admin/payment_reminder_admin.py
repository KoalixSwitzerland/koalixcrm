# -*- coding: utf-8 -*-

from django.utils.translation import gettext as _
from koalixcrm.plugin import *
from koalixcrm.contracts.admin.sales_document_admin import OptionSalesDocument


class OptionPaymentReminder(OptionSalesDocument):
    list_display = OptionSalesDocument.list_display + ('payable_until',
                                                       'status',
                                                       'iteration_number')
    list_filter = OptionSalesDocument.list_filter + ('status',)
    ordering = OptionSalesDocument.ordering
    search_fields = OptionSalesDocument.search_fields
    fieldsets = OptionSalesDocument.fieldsets + (
        (_('Quote specific'), {
            'fields': ('payable_until',
                       'status',
                       'payment_bank_reference',
                       'iteration_number')
        }),
    )

    save_as = OptionSalesDocument.save_as
    inlines = OptionSalesDocument.inlines
    actions = ['create_purchase_confirmation',
               'create_invoice',
               'create_quote',
               'create_delivery_note',
               'create_pdf',
               'register_invoice_in_accounting',
               'register_payment_in_accounting']

    pluginProcessor = PluginProcessor()
    inlines.extend(pluginProcessor.getPluginAdditions("quoteInlines"))
