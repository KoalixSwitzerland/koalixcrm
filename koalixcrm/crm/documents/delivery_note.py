# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import gettext as _
from koalixcrm.crm.const.status import *
from koalixcrm.crm.documents.sales_document import SalesDocument, OptionSalesDocument


class DeliveryNote(SalesDocument):
    tracking_reference = models.CharField(verbose_name=_("Tracking Reference"), max_length=100, blank=True)
    status = models.CharField(max_length=1, choices=DELIVERYNOTESTATUS)

    def create_from_reference(self, calling_model):
        self.create_sales_document(calling_model)
        self.status = 'C'
        self.template_set = self.contract.get_template_set(self)
        self.save()
        self.attach_sales_document_positions(calling_model)
        self.attach_text_paragraphs()

    def __str__(self):
        return _("Delivery Note") + ": " + self.id.__str__() + " " + _("from Contract") + ": " + self.contract.id.__str__()

    class Meta:
        app_label = "crm"
        verbose_name = _('Delivery Note')
        verbose_name_plural = _('Delivery Notes')


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
    actions = ['create_purchase_confirmation', 'create_invoice','create_pdf']
