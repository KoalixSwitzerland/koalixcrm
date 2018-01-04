# -*- coding: utf-8 -*-

from datetime import *
from django.db import models
from django.utils.translation import ugettext as _
from koalixcrm.crm.const.status import *
from koalixcrm.crm.exceptions import *
from koalixcrm import accounting
from koalixcrm.crm.documents.salescontract import SalesContract
from koalixcrm.crm.documents.salescontract import TextParagraphInSalesContract
from koalixcrm.crm.documents.salescontractposition import SalesContractPosition
from koalixcrm.djangoUserExtension.models import TextParagraphInDocumentTemplate
import koalixcrm.crm.documents.pdfexport


class Invoice(SalesContract):
    payableuntil = models.DateField(verbose_name=_("To pay until"))
    derivatedFromQuote = models.ForeignKey("Quote", blank=True, null=True)
    paymentBankReference = models.CharField(verbose_name=_("Payment Bank Reference"), max_length=100, blank=True,
                                            null=True)
    status = models.CharField(max_length=1, choices=INVOICESTATUS)

    def create_invoice(self, calling_model):
        """Checks which model was calling the function. Depending on the calling
        model, the function sets up an invoice. On success, the invoice is saved.
        At the moment only the koalixcrm.crm.documents.contract.Contract and
        koalixcrm.crm.documents.quote.Quote are allowed to call this function"""

        self.staff = calling_model.staff
        if type(calling_model) == koalixcrm.crm.documents.contract.Contract:
            self.contract = calling_model
            self.customer = calling_model.defaultcustomer
            self.currency = calling_model.defaultcurrency
            self.description = calling_model.description
            self.discount = 0
        elif type(calling_model) == koalixcrm.crm.documents.quote.Quote:
            self.contract = calling_model.contract
            self.derivatedFromQuote = calling_model
            self.customer = calling_model.customer
            self.currency = calling_model.currency
            self.discount = calling_model.discount
            self.description = calling_model.description

        self.status = 'C'
        self.payableuntil = date.today() + \
                            timedelta(days=self.customer.defaultCustomerBillingCycle.timeToPaymentDate)
        self.dateofcreation = date.today().__str__()
        self.save()

        if type(calling_model) == koalixcrm.crm.documents.contract.Contract:
            invoice_template_id = calling_model.default_template_set.invoice_template.id
            default_paragraphs = TextParagraphInDocumentTemplate.objects.filter(document_template=invoice_template_id)
            for default_paragraph in list(default_paragraphs):
                invoice_paragraph = TextParagraphInSalesContract()
                invoice_paragraph.create_paragraph(default_paragraph, self)

        if type(calling_model) == koalixcrm.crm.documents.quote.Quote:
            quote_positions = SalesContractPosition.objects.filter(contract=calling_model.id)
            for quote_position in list(quote_positions):
                invoice_position = SalesContractPosition()
                invoice_position.create_position(quote_position, self)
            quote_paragraphs = TextParagraphInSalesContract.objects.filter(sales_contract=calling_model.id)
            for quote_paragraph in list(quote_paragraphs):
                invoice_paragraph = TextParagraphInSalesContract()
                invoice_paragraph.create_paragraph(quote_paragraph, self)

    def is_complete_with_price(self):
        """ Checks whether the Invoice is completed with a price, in case the invoice
        was not completed or the price calculation was not performed, the method
        returns false"""

        if self.lastPricingDate and self.lastCalculatedPrice:
            return True
        else:
            return False

    def registerinvoiceinaccounting(self, request):
        dictprices = dict()
        dicttax = dict()
        currentValidAccountingPeriod = accounting.models.AccountingPeriod.getCurrentValidAccountingPeriod()
        activaaccount = accounting.models.Account.objects.filter(isopeninterestaccount=True)
        if not self.is_complete_with_price():
            raise IncompleteInvoice(_("Complete invoice and run price recalculation. Price may not be Zero"))
        if len(activaaccount) == 0:
            raise OpenInterestAccountMissing(_("Please specify one open intrest account in the accounting"))
        for position in list(SalesContractPosition.objects.filter(contract=self.id)):
            profitaccount = position.product.accoutingProductCategorie.profitAccount
            dictprices[profitaccount] = position.lastCalculatedPrice
            dicttax[profitaccount] = position.lastCalculatedTax

        for booking in accounting.models.Booking.objects.filter(accountingPeriod=currentValidAccountingPeriod):
            if booking.bookingReference == self:
                raise InvoiceAlreadyRegistered()
        for profitaccount, amount in iter(dictprices.items()):
            booking = accounting.models.Booking()
            booking.toAccount = activaaccount[0]
            booking.fromAccount = profitaccount
            booking.bookingReference = self
            booking.accountingPeriod = currentValidAccountingPeriod
            booking.bookingDate = date.today().__str__()
            booking.staff = request.user
            booking.amount = amount
            booking.lastmodifiedby = request.user
            booking.save()

    def registerpaymentinaccounting(self, request, amount, paymentaccount):
        currentValidAccountingPeriod = accounting.models.AccountingPeriod.getCurrentValidAccountingPeriod()
        activaaccount = accounting.models.Account.objects.filter(isopeninterestaccount=True)
        booking = accounting.models.Booking()
        booking.toAccount = paymentaccount
        booking.fromAccount = activaaccount[0]
        booking.bookingDate = date.today().__str__()
        booking.bookingReference = self
        booking.accountingPeriod = currentValidAccountingPeriod
        booking.amount = self.lastCalculatedPrice
        booking.staff = request.user
        booking.lastmodifiedby = request.user
        booking.save()

    def createPDF(self):
        self.last_print_date = datetime.now()
        self.save()
        return koalixcrm.crm.documents.pdfexport.PDFExport.createPDF(self)

    def __str__(self):
        return _("Invoice") + ": " + str(self.id) + " " + _("from Contract") + ": " + str(self.contract.id)

    class Meta:
        app_label = "crm"
        verbose_name = _('Invoice')
        verbose_name_plural = _('Invoices')