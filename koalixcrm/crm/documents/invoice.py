# -*- coding: utf-8 -*-

from datetime import *
from django import forms
from django.db import models
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from koalixcrm.crm.const.status import *
from koalixcrm.crm.exceptions import *
from koalixcrm import accounting
from koalixcrm.crm.documents.salesdocument import SalesDocument, OptionSalesDocument
from koalixcrm.crm.documents.salesdocumentposition import SalesDocumentPosition
from koalixcrm.plugin import *
from koalixcrm.accounting.models import Account
from django.contrib.admin import helpers
from django.shortcuts import render
from django.template.context_processors import csrf


class Invoice(SalesDocument):
    payable_until = models.DateField(verbose_name=_("To pay until"))
    payment_bank_reference = models.CharField(verbose_name=_("Payment Bank Reference"), max_length=100, blank=True,
                                              null=True)
    status = models.CharField(max_length=1, choices=INVOICESTATUS)

    def create_invoice(self, calling_model):
        """Checks which model was calling the function. Depending on the calling
        model, the function sets up an invoice. On success, the invoice is saved.
        At the moment only the koalixcrm.crm.documents.contract.Contract and
        koalixcrm.crm.documents.quote.Quote are allowed to call this function"""

        self.create_sales_document(calling_model)

        self.status = 'C'
        self.payable_until = date.today() + \
                             timedelta(days=self.customer.defaultCustomerBillingCycle.timeToPaymentDate)
        self.date_of_creation = date.today().__str__()

        self.template_set = self.contract.default_template_set.invoice_template
        self.save()
        self.attach_sales_document_positions(calling_model)
        self.attach_text_paragraphs()

    def register_invoice_in_accounting(self, request):
        dict_prices = dict()
        dict_tax = dict()
        current_valid_accounting_period = accounting.models.AccountingPeriod.getCurrentValidAccountingPeriod()
        activa_account = accounting.models.Account.objects.filter(isopeninterestaccount=True)
        if not self.is_complete_with_price():
            raise IncompleteInvoice(_("Complete invoice and run price recalculation. Price may not be Zero"))
        if len(activa_account) == 0:
            raise OpenInterestAccountMissing(_("Please specify one open intrest account in the accounting"))
        for position in list(SalesDocumentPosition.objects.filter(contract=self.id)):
            profit_account = position.product.accoutingProductCategorie.profitAccount
            dict_prices[profit_account] = position.lastCalculatedPrice
            dict_tax[profit_account] = position.lastCalculatedTax

        for booking in accounting.models.Booking.objects.filter(accountingPeriod=currentValidAccountingPeriod):
            if booking.bookingReference == self:
                raise InvoiceAlreadyRegistered()
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

    def register_payment_in_accounting(self, request, amount, paymentaccount):
        current_valid_accounting_period = accounting.models.AccountingPeriod.getCurrentValidAccountingPeriod()
        activa_account = accounting.models.Account.objects.filter(isopeninterestaccount=True)
        booking = accounting.models.Booking()
        booking.toAccount = paymentaccount
        booking.fromAccount = activa_account[0]
        booking.bookingDate = date.today().__str__()
        booking.bookingReference = self
        booking.accountingPeriod = current_valid_accounting_period
        booking.amount = self.last_calculated_price
        booking.staff = request.user
        booking.lastmodifiedby = request.user
        booking.save()

    def __str__(self):
        return _("Invoice") + ": " + str(self.id) + " " + _("from Contract") + ": " + str(self.contract.id)

    class Meta:
        app_label = "crm"
        verbose_name = _('Invoice')
        verbose_name_plural = _('Invoices')


class OptionInvoice(OptionSalesDocument):
    list_display = OptionSalesDocument.list_display + ('payable_until', 'status',)
    list_filter = OptionSalesDocument.list_filter + ('status',)
    ordering = OptionSalesDocument.ordering
    search_fields = OptionSalesDocument.search_fields
    fieldsets = OptionSalesDocument.fieldsets + (
        (_('Invoice specific'), {
            'fields': ( 'payable_until', 'status', 'payment_bank_reference' )
        }),
    )

    class PaymentForm(forms.Form):
        paymentAmount = forms.DecimalField()
        _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
        paymentAccount = forms.ModelChoiceField(Account.objects.filter(accountType="A"))

    def register_invoice_in_accounting(self, request, queryset):
        try:
            for obj in queryset:
                obj.register_invoice_in_accounting(request)
            self.message_user(request, _("Successfully registered Invoice in the Accounting"))
            return;
        except OpenInterestAccountMissing as e:
            self.message_user(request, "Did not register Invoice in Accounting: " + e.__str__(), level=messages.ERROR)
            return;
        except IncompleteInvoice as e:
            self.message_user(request, "Did not register Invoice in Accounting: " + e.__str__(), level=messages.ERROR)
            return;

    register_invoice_in_accounting.short_description = _("Register Invoice in Accounting")

    # def unregisterInvoiceInAccounting(self, request, queryset):
    # for obj in queryset:
    # obj.createPDF(deliveryorder=True)
    # self.message_user(request, _("Successfully unregistered Invoice in the Accounting"))
    # unregisterInvoiceInAccounting.short_description = _("Unregister Invoice in Accounting")

    def register_payment_in_accounting(self, request, queryset):
        form = None
        if request.POST.get('post'):
            if 'cancel' in request.POST:
                self.message_user(request, _("Canceled registeration of payment in the accounting"), level=messages.ERROR)
                return
            elif 'register' in request.POST:
                form = self.PaymentForm(request.POST)
                if form.is_valid():
                    payment_amount = form.cleaned_data['paymentAmount']
                    payment_account = form.cleaned_data['paymentAccount']
                    for obj in queryset:
                        obj.register_payment_in_accounting(request, payment_amount, payment_account)
                    self.message_user(request, _("Successfully registered Payment in the Accounting"))
                    return HttpResponseRedirect(request.get_full_path())
        else:
            form = self.PaymentForm
            c = {'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME, 'queryset': queryset, 'form': form}
            c.update(csrf(request))
            return render(request, 'crm/admin/registerPayment.html', c)

    register_payment_in_accounting.short_description = _("Register Payment in Accounting")

    save_as = OptionSalesDocument.save_as
    inlines = OptionSalesDocument.inlines

    actions = ['create_purchase_confirmation', 'create_invoice', 'create_quote',
               'create_delivery_note', 'create_pdf', 'create_payment_reminder',
               'register_invoice_in_accounting', 'register_payment_in_accounting',]

    pluginProcessor = PluginProcessor()
    actions.extend(pluginProcessor.getPluginAdditions("invoiceActions"))
    inlines.extend(pluginProcessor.getPluginAdditions("invoiceInlines"))


class InlineInvoice(admin.TabularInline):
    model = Invoice
    classes = ['collapse']
    show_change_link = True
    can_delete = True
    extra = 1
    readonly_fields = (
    'last_pricing_date', 'last_calculated_price', 'last_calculated_tax', 'description', 'contract', 'customer',
    'payable_until', 'status')
    fieldsets = (
        (_('Basics'), {
            'fields': ('description', 'contract', 'customer', 'payable_until', 'status'),
        }),
        (_('Advanced (not editable)'), {
            'classes': ('collapse',),
            'fields': ('last_pricing_date', 'last_calculated_price', 'last_calculated_tax',)
        }),
    )

    allow_add = False
