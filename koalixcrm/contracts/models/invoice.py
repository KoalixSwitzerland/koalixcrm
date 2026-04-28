# -*- coding: utf-8 -*-
from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal
from typing import TYPE_CHECKING

from django.db import models
from django.utils.html import format_html
from django.utils.translation import gettext as _

from koalixcrm.contracts.models.commercial_document import CommercialDocument
from koalixcrm.contracts.models.commercial_document_position import (
    CommercialDocumentPosition,
)
from koalixcrm.core.const.status import *
from koalixcrm.core.exceptions import *
from koalixcrm.global_support_functions import limit_string_length

if TYPE_CHECKING:
    from django.http import HttpRequest

    from koalixcrm.accounting.models.account import Account


class Invoice(CommercialDocument):
    payable_until = models.DateField(verbose_name=_("To pay until"))
    payment_bank_reference = models.CharField(verbose_name=_("Payment Bank Reference"), max_length=100, blank=True,
                                              null=True)
    status = models.CharField(max_length=1, choices=INVOICESTATUS)

    def link_to_invoice(self) -> str:
        if self.id:
            return format_html("<a href='/admin/contract_object_management/invoice/%s' >%s</a>" % (str(self.id),
                                                                            limit_string_length(str(self.description),
                                                                                                30)))
        else:
            return "Not present"
    link_to_invoice.short_description = _("Invoice")

    def create_from_reference(self, calling_model: models.Model) -> None:
        self.create_commercial_document(calling_model)
        self.status = 'C'
        cycle = self.party.default_billing_cycle
        self.payable_until = date.today() + timedelta(days=cycle.time_to_payment_date)
        self.date_of_creation = date.today().__str__()
        self.template_set = self.contract.get_template_set(self)
        self.save()
        self.attach_commercial_document_positions(calling_model)
        self.attach_text_paragraphs()

    def register_invoice_in_accounting(self, request: HttpRequest) -> None:
        from koalixcrm import accounting  # local import: accounting is an optional plugin
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

    def register_payment_in_accounting(
        self, request: HttpRequest, amount: Decimal, payment_account: Account
    ) -> None:
        from koalixcrm import accounting  # local import: accounting is an optional plugin
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

    def __str__(self) -> str:
        return _("Invoice") + ": " + str(self.id) + " " + _("from Contract") + ": " + str(self.contract.id)

    class Meta:
        app_label = "contract_object_management"
        db_table = "crm_invoice"
        verbose_name = _('Invoice')
        verbose_name_plural = _('Invoices')
