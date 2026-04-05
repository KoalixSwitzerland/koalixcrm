# -*- coding: utf-8 -*-

from koalixcrm.contracts.admin.sales_document_admin import OptionSalesDocument


class OptionPurchaseConfirmation(OptionSalesDocument):
    list_display = OptionSalesDocument.list_display
    list_filter = OptionSalesDocument.list_filter
    ordering = OptionSalesDocument.ordering
    search_fields = OptionSalesDocument.search_fields
    fieldsets = OptionSalesDocument.fieldsets

    save_as = OptionSalesDocument.save_as
    inlines = OptionSalesDocument.inlines
    actions = ['create_invoice', 'create_quote',
               'create_delivery_note', 'create_purchase_order', 'create_', 'create_pdf']
