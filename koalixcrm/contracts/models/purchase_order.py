# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import gettext as _
from koalixcrm.core.const.status import *
from koalixcrm.contracts.models.commercial_document import CommercialDocument


class PurchaseOrder(CommercialDocument):
    supplier = models.ForeignKey("contacts.Supplier", on_delete=models.CASCADE, verbose_name=_("Supplier"), null=True)
    status = models.CharField(max_length=1, choices=PURCHASEORDERSTATUS)

    def create_from_reference(self, calling_model):
        self.create_commercial_document(calling_model)
        self.status = 'O'
        self.template_set = self.contract.get_template_set(self)
        self.save()
        self.attach_commercial_document_positions(calling_model)
        self.attach_text_paragraphs()
        self.staff = calling_model.staff

    def __str__(self):
        return _("Purchase Order") + ": " + self.id.__str__() + " " + _("from Contract") + ": " + self.contract.id.__str__()

    class Meta:
        app_label = "contract_object_management"
        db_table = "crm_purchaseorder"
        verbose_name = _('Purchase Order')
        verbose_name_plural = _('Purchase Orders')
