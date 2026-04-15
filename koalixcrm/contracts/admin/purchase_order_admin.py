# -*- coding: utf-8 -*-

from django.utils.translation import gettext as _
from koalixcrm.plugin import *
from koalixcrm.contracts.admin.commercial_document_admin import OptionCommercialDocument


class OptionPurchaseOrder(OptionCommercialDocument):
    list_display = OptionCommercialDocument.list_display + ('supplier', 'status',)
    list_filter = OptionCommercialDocument.list_filter + ('status',)
    ordering = OptionCommercialDocument.ordering
    search_fields = OptionCommercialDocument.search_fields
    fieldsets = OptionCommercialDocument.fieldsets + (
        (_('Purchase Order specific'), {
            'fields': ('supplier', 'status',)
        }),
    )

    save_as = OptionCommercialDocument.save_as
    inlines = OptionCommercialDocument.inlines
    actions = ['create_purchase_confirmation', 'create_invoice', 'create_quote',
               'create_delivery_note', 'create_pdf_async',
               'register_invoice_in_accounting', 'register_payment_in_accounting',]

    pluginProcessor = PluginProcessor()
    inlines.extend(pluginProcessor.getPluginAdditions("quoteInlines"))
