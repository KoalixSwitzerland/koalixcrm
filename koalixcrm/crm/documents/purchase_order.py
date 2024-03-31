# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import gettext as _
from koalixcrm.crm.const.status import *
from koalixcrm.crm.documents.sales_document import SalesDocument, OptionSalesDocument
from koalixcrm.plugin import *


class PurchaseOrder(SalesDocument):
    supplier = models.ForeignKey("Supplier", on_delete=models.CASCADE, verbose_name=_("Supplier"), null=True)
    status = models.CharField(max_length=1, choices=PURCHASEORDERSTATUS)

    def create_from_reference(self, calling_model):
        self.create_sales_document(calling_model)
        self.status = 'O'
        self.template_set = self.contract.get_template_set(self)
        self.save()
        self.attach_sales_document_positions(calling_model)
        self.attach_text_paragraphs()
        self.staff = calling_model.staff

    def __str__(self):
        return _("Purchase Order") + ": " + self.id.__str__() + " " + _("from Contract") + ": " + self.contract.id.__str__()

    class Meta:
        app_label = "crm"
        verbose_name = _('Purchase Order')
        verbose_name_plural = _('Purchase Orders')


class OptionPurchaseOrder(OptionSalesDocument):
    list_display = OptionSalesDocument.list_display + ('supplier', 'status',)
    list_filter = OptionSalesDocument.list_filter + ('status',)
    ordering = OptionSalesDocument.ordering
    search_fields = OptionSalesDocument.search_fields
    fieldsets = OptionSalesDocument.fieldsets + (
        (_('Purchase Order specific'), {
            'fields': ('supplier', 'status',)
        }),
    )

    save_as = OptionSalesDocument.save_as
    inlines = OptionSalesDocument.inlines
    actions = ['create_purchase_confirmation', 'create_invoice', 'create_quote',
               'create_delivery_note', 'create_pdf',
               'register_invoice_in_accounting', 'register_payment_in_accounting',]

    pluginProcessor = PluginProcessor()
    inlines.extend(pluginProcessor.getPluginAdditions("quoteInlines"))
