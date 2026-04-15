# -*- coding: utf-8 -*-

from django.utils.translation import gettext as _
from koalixcrm.contracts.admin.sales_document_admin import OptionSalesDocument


class OptionDeliveryNote(OptionSalesDocument):
    list_display = OptionSalesDocument.list_display + ('status',)
    list_filter = OptionSalesDocument.list_filter + ('status',)
    ordering = OptionSalesDocument.ordering
    search_fields = OptionSalesDocument.search_fields
    fieldsets = OptionSalesDocument.fieldsets + (
        (_('Delivery Note specific'), {
            'fields': ('status', )
        }),
    )

    save_as = OptionSalesDocument.save_as
    inlines = OptionSalesDocument.inlines
    actions = ['create_purchase_confirmation', 'create_invoice', 'create_pdf_async']
