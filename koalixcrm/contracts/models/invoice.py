# -*- coding: utf-8 -*-

from datetime import date, timedelta
from django.db import models
from django.utils.translation import gettext as _
from django.utils.html import format_html
from koalixcrm.core.const.status import INVOICESTATUS
from koalixcrm.core.exceptions import IncompleteInvoice, OpenInterestAccountMissing, InvoiceAlreadyRegistered
from koalixcrm import accounting
from koalixcrm.contracts.models.commercial_document import CommercialDocument
from koalixcrm.contracts.models.commercial_document_position import CommercialDocumentPosition
from koalixcrm.global_support_functions import limit_string_length


class Invoice(CommercialDocument):
    payable_until = models.DateField(verbose_name=_("To pay until"))
    payment_bank_reference = models.CharField(verbose_name=_("Payment Bank Reference"), max_length=100, blank=True,
                                              null=True)
    status = models.CharField(max_length=1, choices=INVOICESTATUS)

    def link_to_invoice(self):
        if self.id:
            return format_html("<a href='/admin/contract_object_management/invoice/%s' >%s</a>" % (str(self.id),
                                                                            limit_string_length(str(self.description),
                                                                                                30)))
        else:
            return "Not present"
    link_to_invoice.short_description = _("Invoice")

    def create_from_reference(self, calling_model):
        self.create_commercial_document(calling_model)
        self.status = 'C'
        self.payable_until = date.today() + \
                             timedelta(days=self.customer.default_customer_billing_cycle.time_to_payment_date)
        self.date_of_creation = date.today().__str__()
        self.template_set = self.contract.get_template_set(self)
        self.save()
        self.attach_commercial_document_positions(calling_model)
        self.attach_text_paragraphs()

    def register_invoice_in_accounting(self, request):
        dict_prices = dict()
        dict_tax = dict()
        current_valid_accounting_period = accounting.models.AccountingPeriod.get_current_valid_accounting_period()
        activa_account = accounting.models.Account.objects.filter(isopeninterestaccount=True)
        if not self.is_complete_with_price():
            raise IncompleteInvoice(_("Complete invoice and run price recalculation. Price may not be Zero"))
        if len(activa_account) == 0:
            raise OpenInterestAccountMissing(_("Please specify one open interest account in the accounting"))
        for position in list(CommercialDocumentPosition.objects.filter(commercial_document=self.id)):
            profit_account = position.product.accounting_product_categorie.profitAccount
            dict_prices[profit_account] = position.last_calculated_price
            dict_tax[profit_account] = position.last_calculated_tax

        for booking in accounting.models.Booking.objects.filter(accountingPeriod=current_valid_accounting_period):
            if booking.bookingReference == self:
                raise InvoiceAlreadyRegistered("The invoice is already registered")
        for profit_account, amount in iter(dict_prices.items()):
            booking = accounting.models.Booking()
            booking.toAccount = activa_account[0]
            booking.fromAccount = profit_account
            booking.bookingReference = self
            booking.accountingPeriod = current_valid_accounting_period
            booking.bookingDate = date.today().__str__()
            booking.staff = request.user
            booking.amount = amount
            booking.lastmodifiedby = request.user
            booking.save()

    def register_payment_in_accounting(self, request, amount, payment_account):
        current_valid_accounting_period = accounting.models.AccountingPeriod.get_current_valid_accounting_period()
        activa_account = accounting.models.Account.objects.filter(isopeninterestaccount=True)
        booking = accounting.models.Booking()
        booking.toAccount = payment_account
        booking.fromAccount = activa_account[0]
        booking.bookingDate = date.today().__str__()
        booking.bookingReference = self
        booking.accountingPeriod = current_valid_accounting_period
        booking.amount = amount
        booking.staff = request.user
        booking.lastmodifiedby = request.user
        booking.save()

    def __str__(self):
        return _("Invoice") + ": " + self.id.__str__() + " " + _("from Contract") + ": " + self.contract.id.__str__()

    class Meta:
        app_label = "contract_object_management"
        db_table = "crm_invoice"
        verbose_name = _('Invoice')
        verbose_name_plural = _('Invoices')
