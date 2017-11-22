# -*- coding: utf-8 -*-

from datetime import *
from django.db import models
from django.utils.translation import ugettext as _
from koalixcrm.crm.const.status import *
from koalixcrm.crm.documents.salescontract import SalesContract
import koalixcrm.crm.documents.pdfexport


class DeliveryNote(SalesContract):
    derived_from_invoice = models.ForeignKey("Invoice", blank=True, null=True)
    status = models.CharField(max_length=1, choices=DELIVERYNOTESTATUS)

    def createPDF(self):
        self.last_print_date = datetime.now()
        self.save()
        return koalixcrm.crm.documents.pdfexport.PDFExport.createPDF(self)

    def __str__(self):
        return _("Delivery Note") + ": " + str(self.id) + " " + _("from Contract") + ": " + str(self.contract.id)

    class Meta:
        app_label = "crm"
        verbose_name = _('Delivery Note')
        verbose_name_plural = _('Delivery Notes')