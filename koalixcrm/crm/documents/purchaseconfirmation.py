# -*- coding: utf-8 -*-

from datetime import *
from django.utils.translation import ugettext as _
from koalixcrm.crm.documents.salesdocument import SalesDocument, OptionSalesDocument


class PurchaseConfirmation(SalesDocument):

    def create_purchase_confirmation(self, calling_model):
        self.create_sales_document(calling_model)
        self.template_set = self.contract.default_template_set.purchase_confirmation_template
        self.save()
        self.attach_sales_document_positions(calling_model)
        self.attach_text_paragraphs()

    def __str__(self):
        return _("Purchase Confirmation") + ": " + str(self.id) + " " + _("from Contract") + ": " + str(self.contract.id)

    class Meta:
        app_label = "crm"
        verbose_name = _('Purchase Confirmation')
        verbose_name_plural = _('Purchase Confirmations')


class OptionPurchaseConfirmation(OptionSalesDocument):
    list_display = OptionSalesDocument.list_display
    list_filter = OptionSalesDocument.list_filter
    ordering = OptionSalesDocument.ordering
    search_fields = OptionSalesDocument.search_fields
    fieldsets = OptionSalesDocument.fieldsets

    save_as = OptionSalesDocument.save_as
    inlines = OptionSalesDocument.inlines
    actions = ['create_invoice', 'create_quote',
               'create_delivery_note', 'create_purchase_order', 'create_pdf']
