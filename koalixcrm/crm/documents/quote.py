# -*- coding: utf-8 -*-

from datetime import *
from django.db import models
from django.utils.translation import ugettext as _
from koalixcrm.crm.const.status import *
from koalixcrm.crm.documents.salescontract import SalesContract
from koalixcrm.crm.documents.salescontractposition import SalesContractPosition
import koalixcrm.crm.documents.invoice
import koalixcrm.crm.documents.pdfexport

class Quote(SalesContract):
    valid_until = models.DateField(verbose_name=_("Valid until"))
    status = models.CharField(max_length=1, choices=QUOTESTATUS, verbose_name=_('Status'))

    def createInvoice(self):
        invoice = koalixcrm.crm.documents.invoice.Invoice()
        invoice.create_invoice(self)
        return invoice

    def create_quote(self, calling_model):
        self.contract = calling_model
        self.discount = 0
        self.staff = calling_model.staff
        self.customer = calling_model.defaultcustomer
        self.status = 'C'
        self.currency = calling_model.defaultcurrency
        self.valid_until = date.today().__str__()
        self.date_of_creation = date.today().__str__()
        self.save()

    def createPDF(self):
        self.last_print_date = datetime.now()
        self.save()
        return koalixcrm.crm.documents.pdfexport.PDFExport.createPDF(self)

    def __str__(self):
        return _("Quote") + ": " + str(self.id) + " " + _("from Contract") + ": " + str(self.contract.id)

    class Meta:
        app_label = "crm"
        verbose_name = _('Quote')
        verbose_name_plural = _('Quotes')
