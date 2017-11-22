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
    validuntil = models.DateField(verbose_name=_("Valid until"))
    status = models.CharField(max_length=1, choices=QUOTESTATUS, verbose_name=_('Status'))

    def createInvoice(self):
        invoice = koalixcrm.crm.documents.invoice.Invoice()
        invoice.contract = self.contract
        invoice.description = self.description
        invoice.discount = self.discount
        invoice.customer = self.customer
        invoice.staff = self.staff
        invoice.status = 'C'
        invoice.derivatedFromQuote = self
        invoice.currency = self.currency
        invoice.payableuntil = date.today() + timedelta(
            days=self.customer.defaultCustomerBillingCycle.timeToPaymentDate)
        invoice.dateofcreation = date.today().__str__()
        invoice.customerBillingCycle = self.customer.defaultCustomerBillingCycle
        invoice.save()
        try:
            quotePositions = SalesContractPosition.objects.filter(contract=self.id)
            for quotePosition in list(quotePositions):
                invoicePosition = SalesContractPosition()
                invoicePosition.product = quotePosition.product
                invoicePosition.positionNumber = quotePosition.positionNumber
                invoicePosition.quantity = quotePosition.quantity
                invoicePosition.description = quotePosition.description
                invoicePosition.discount = quotePosition.discount
                invoicePosition.product = quotePosition.product
                invoicePosition.unit = quotePosition.unit
                invoicePosition.sentOn = quotePosition.sentOn
                invoicePosition.supplier = quotePosition.supplier
                invoicePosition.shipmentID = quotePosition.shipmentID
                invoicePosition.overwriteProductPrice = quotePosition.overwriteProductPrice
                invoicePosition.positionPricePerUnit = quotePosition.positionPricePerUnit
                invoicePosition.lastPricingDate = quotePosition.lastPricingDate
                invoicePosition.lastCalculatedPrice = quotePosition.lastCalculatedPrice
                invoicePosition.lastCalculatedTax = quotePosition.lastCalculatedTax
                invoicePosition.contract = invoice
                invoicePosition.save()
            return invoice
        except Quote.DoesNotExist:
            return

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
