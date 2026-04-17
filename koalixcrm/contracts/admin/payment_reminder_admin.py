# -*- coding: utf-8 -*-

from django.utils.translation import gettext as _
from koalixcrm.plugin import *  # noqa: F401, F403
from koalixcrm.contracts.admin.commercial_document_admin import OptionCommercialDocument


class OptionPaymentReminder(OptionCommercialDocument):
    list_display = OptionCommercialDocument.list_display + ('payable_until',
                                                       'status',
                                                       'iteration_number')
    list_filter = OptionCommercialDocument.list_filter + ('status',)
    ordering = OptionCommercialDocument.ordering
    search_fields = OptionCommercialDocument.search_fields
    fieldsets = OptionCommercialDocument.fieldsets + (
        (_('Payment Reminder specific'), {
            'fields': ('payable_until',
                       'status',
                       'payment_bank_reference',
                       'iteration_number')
        }),
    )

    save_as = OptionCommercialDocument.save_as
    inlines = OptionCommercialDocument.inlines
    actions = ['create_sales_order',
               'create_invoice',
               'create_quotation',
               'create_despatch_advice',
               'create_pdf_async',
               'register_invoice_in_accounting',
               'register_payment_in_accounting']

    pluginProcessor = PluginProcessor()  # noqa: F405
    inlines.extend(pluginProcessor.getPluginAdditions("quotationInlines"))
