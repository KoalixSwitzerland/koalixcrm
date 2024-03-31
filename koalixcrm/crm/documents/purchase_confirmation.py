# -*- coding: utf-8 -*-

from django.utils.translation import gettext as _
from koalixcrm.crm.documents.sales_document import SalesDocument, OptionSalesDocument


class PurchaseConfirmation(SalesDocument):

    def create_from_reference(self, calling_model):
        self.create_sales_document(calling_model)
        self.template_set = self.contract.get_template_set(self)
        self.save()
        self.attach_sales_document_positions(calling_model)
        self.attach_text_paragraphs()

    def __str__(self):
        return _("Purchase Confirmation") + ": " + self.id.__str__() + " " + _("from Contract") + ": " + self.contract.id.__str__()

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
               'create_delivery_note', 'create_purchase_order', 'create_', 'create_pdf']
