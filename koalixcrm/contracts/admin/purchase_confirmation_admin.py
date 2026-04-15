# -*- coding: utf-8 -*-

from koalixcrm.contracts.admin.commercial_document_admin import OptionCommercialDocument


class OptionPurchaseConfirmation(OptionCommercialDocument):
    list_display = OptionCommercialDocument.list_display
    list_filter = OptionCommercialDocument.list_filter
    ordering = OptionCommercialDocument.ordering
    search_fields = OptionCommercialDocument.search_fields
    fieldsets = OptionCommercialDocument.fieldsets

    save_as = OptionCommercialDocument.save_as
    inlines = OptionCommercialDocument.inlines
    actions = ['create_invoice', 'create_quote',
               'create_delivery_note', 'create_purchase_order', 'create_pdf_async']
