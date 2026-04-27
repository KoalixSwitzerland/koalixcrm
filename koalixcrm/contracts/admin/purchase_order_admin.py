# -*- coding: utf-8 -*-

from django.utils.translation import gettext as _

from koalixcrm.contracts.admin.commercial_document_admin import OptionCommercialDocument
from koalixcrm.plugin import *


class OptionPurchaseOrder(OptionCommercialDocument):
    # PurchaseOrder uses the inherited CommercialDocument.party as the
    # supplier (no separate supplier field since v2.0.0 / issue #395 G3).
    list_display = OptionCommercialDocument.list_display + ('status',)
    list_filter = OptionCommercialDocument.list_filter + ('status',)
    ordering = OptionCommercialDocument.ordering
    search_fields = OptionCommercialDocument.search_fields
    fieldsets = OptionCommercialDocument.fieldsets + (
        (_('Purchase Order specific'), {
            'fields': ('status',)
        }),
    )

    save_as = OptionCommercialDocument.save_as
    inlines = OptionCommercialDocument.inlines
    actions = ['create_sales_order', 'create_invoice', 'create_quotation',
               'create_despatch_advice', 'create_pdf_async',
               'register_invoice_in_accounting', 'register_payment_in_accounting',]

    pluginProcessor = PluginProcessor()
    inlines.extend(pluginProcessor.getPluginAdditions("quotationInlines"))
