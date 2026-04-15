# -*- coding: utf-8 -*-

from datetime import *
from django.db import models
from django.utils.translation import gettext as _
from django.utils.html import format_html
from koalixcrm.crm.const.status import *
from koalixcrm.crm.exceptions import *
from koalixcrm import accounting
from koalixcrm.contracts.models.commercial_document import CommercialDocument
from koalixcrm.contracts.models.commercial_document_position import CommercialDocumentPosition
from koalixcrm.global_support_functions import limit_string_length


class CreditNote(CommercialDocument):
    corrects_invoice = models.ForeignKey(
        "Invoice",
        on_delete=models.PROTECT,
        verbose_name=_("Corrects Invoice"),
        null=True,
        blank=True,
    )
    status = models.CharField(max_length=1, choices=CREDITNOTESTATUS)
    issue_date = models.DateField(verbose_name=_("Issue Date"))
    reason = models.CharField(
        verbose_name=_("Reason"),
        max_length=200,
        blank=True,
        default="",
    )

    def link_to_credit_note(self):
        if self.id:
            return format_html(
                "<a href='/admin/contract_object_management/creditnote/%s' >%s</a>"
                % (str(self.id), limit_string_length(str(self.description), 30))
            )
        else:
            return "Not present"

    link_to_credit_note.short_description = _("Credit Note")

    def create_from_reference(self, calling_model):
        from koalixcrm.contracts.models.invoice import Invoice

        self.create_commercial_document(calling_model)
        self.status = 'C'
        self.issue_date = date.today()
        if isinstance(calling_model, Invoice):
            self.corrects_invoice = calling_model
        self.template_set = self.contract.get_template_set(self)
        self.save()
        self.attach_commercial_document_positions(calling_model)
        self.attach_text_paragraphs()

    def register_credit_note_in_accounting(self, request):
        dict_prices = dict()
        dict_tax = dict()
        current_valid_accounting_period = accounting.models.AccountingPeriod.get_current_valid_accounting_period()
        activa_account = accounting.models.Account.objects.filter(isopeninterestaccount=True)
        if not self.is_complete_with_price():
            raise IncompleteInvoice(_("Complete credit note and run price recalculation. Price may not be Zero"))
        if len(activa_account) == 0:
            raise OpenInterestAccountMissing(_("Please specify one open interest account in the accounting"))
        for position in list(CommercialDocumentPosition.objects.filter(commercial_document=self.id)):
            profit_account = position.product.accounting_product_categorie.profitAccount
            dict_prices[profit_account] = position.last_calculated_price
            dict_tax[profit_account] = position.last_calculated_tax

        for booking in accounting.models.Booking.objects.filter(accountingPeriod=current_valid_accounting_period):
            if booking.bookingReference == self:
                raise InvoiceAlreadyRegistered("The credit note is already registered")
        for profit_account, amount in iter(dict_prices.items()):
            booking = accounting.models.Booking()
            # Reversed direction compared to Invoice
            booking.toAccount = profit_account
            booking.fromAccount = activa_account[0]
            booking.bookingReference = self
            booking.accountingPeriod = current_valid_accounting_period
            booking.bookingDate = date.today().__str__()
            booking.staff = request.user
            booking.amount = amount
            booking.lastmodifiedby = request.user
            booking.save()

    def __str__(self):
        return (
            _("Credit Note")
            + ": "
            + self.id.__str__()
            + " "
            + _("from Contract")
            + ": "
            + self.contract.id.__str__()
        )

    class Meta:
        app_label = "contract_object_management"
        db_table = "crm_creditnote"
        verbose_name = _('Credit Note')
        verbose_name_plural = _('Credit Notes')
