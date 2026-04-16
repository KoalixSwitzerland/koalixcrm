# -*- coding: utf-8 -*-

from django.utils.translation import gettext as _
from koalixcrm.contracts.admin.commercial_document_admin import OptionCommercialDocument


class OptionDespatchAdvice(OptionCommercialDocument):
    list_display = OptionCommercialDocument.list_display + ('status',)
    list_filter = OptionCommercialDocument.list_filter + ('status',)
    ordering = OptionCommercialDocument.ordering
    search_fields = OptionCommercialDocument.search_fields
    fieldsets = OptionCommercialDocument.fieldsets + (
        (_('Despatch Advice specific'), {
            'fields': ('status', )
        }),
    )

    save_as = OptionCommercialDocument.save_as
    inlines = OptionCommercialDocument.inlines
    actions = ['create_sales_order', 'create_invoice', 'create_pdf_async']
