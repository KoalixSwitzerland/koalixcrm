# -*- coding: utf-8 -*-

from datetime import *
from django import forms
from django.db import models
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.utils.translation import gettext as _
from django.utils.html import format_html
from django.contrib.admin import helpers
from django.shortcuts import render
from django.contrib import messages
from django.template.context_processors import csrf
from koalixcrm.crm.const.status import *
from koalixcrm.crm.exceptions import *
from koalixcrm import accounting
from koalixcrm.crm.documents.sales_document import SalesDocument, OptionSalesDocument
from koalixcrm.crm.documents.sales_document_position import SalesDocumentPosition
from koalixcrm.plugin import *
from koalixcrm.accounting.models import Account
from koalixcrm.global_support_functions import limit_string_length


class Invoice(SalesDocument):
    payable_until = models.DateField(verbose_name=_("To pay until"))
    payment_bank_reference = models.CharField(verbose_name=_("Payment Bank Reference"), max_length=100, blank=True,
                                              null=True)
    status = models.CharField(max_length=1, choices=INVOICESTATUS)

    def link_to_invoice(self):
        if self.id:
            return format_html("<a href='/admin/crm/invoice/%s' >%s</a>" % (str(self.id),
                                                                            limit_string_length(str(self.description),
                                                                                                30)))
        else:
            return "Not present"
    link_to_invoice.short_description = _("Invoice")

    def create_from_reference(self, calling_model):
        self.create_sales_document(calling_model)
        self.status = 'C'
        self.payable_until = date.today() + \
                             timedelta(days=self.customer.default_customer_billing_cycle.time_to_payment_date)
        self.date_of_creation = date.today().__str__()
        self.template_set = self.contract.get_template_set(self)
        self.save()
        self.attach_sales_document_positions(calling_model)
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
        for position in list(SalesDocumentPosition.objects.filter(sales_document=self.id)):
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
            'fields': ('payable_until', 'status', 'payment_bank_reference' )
        }),
    )

    class PaymentForm(forms.Form):
        payment_amount = forms.DecimalField()
        _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
        payment_account = forms.ModelChoiceField(Account.objects.filter(account_type="A"))

    def register_invoice_in_accounting(self, request, queryset):
        try:
            for obj in queryset:
                obj.register_invoice_in_accounting(request)
            self.message_user(request, _("Successfully registered Invoice in the Accounting"))
            return
        except OpenInterestAccountMissing as e:
            self.message_user(request, "Did not register Invoice in Accounting: " + e.__str__(), level=messages.ERROR)
            return
        except IncompleteInvoice as e:
            self.message_user(request, "Did not register Invoice in Accounting: " + e.__str__(), level=messages.ERROR)
            return

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
                self.message_user(request, _("Canceled registration of payment in the accounting"), level=messages.ERROR)
                return
            elif 'register' in request.POST:
                form = self.PaymentForm(request.POST)
                if form.is_valid():
                    payment_amount = form.cleaned_data['payment_amount']
                    payment_account = form.cleaned_data['payment_account']
                    for obj in queryset:
                        obj.register_payment_in_accounting(request, payment_amount, payment_account)
                    self.message_user(request, _("Successfully registered Payment in the Accounting"))
                    return HttpResponseRedirect(request.get_full_path())
        else:
            form = self.PaymentForm
            c = {'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME,
                 'queryset': queryset,
                 'form': form}
            c.update(csrf(request))
            return render(request, 'crm/admin/register_payment.html', c)

    register_payment_in_accounting.short_description = _("Register Payment in Accounting")

    save_as = OptionSalesDocument.save_as
    inlines = OptionSalesDocument.inlines

    actions = ['create_purchase_confirmation',
               'create_quote',
               'create_invoice',
               'create_delivery_note',
               'create_purchase_order',
               'create_payment_reminder',
               'create_pdf',
               'register_invoice_in_accounting',
               'register_payment_in_accounting',]

    pluginProcessor = PluginProcessor()
    actions.extend(pluginProcessor.getPluginAdditions("invoiceActions"))
    inlines.extend(pluginProcessor.getPluginAdditions("invoiceInlines"))


class InlineInvoice(admin.TabularInline):
    model = Invoice
    classes = ['collapse']
    show_change_link = True
    can_delete = True
    extra = 1
    readonly_fields = ('link_to_invoice',
                       'contract',
                       'customer',
                       'payable_until',
                       'status',
                       'last_pricing_date',
                       'last_calculated_price',
                       'last_calculated_tax')
    fieldsets = (
        (_('Invoice'), {
            'fields': ('link_to_invoice',
                       'contract',
                       'customer',
                       'payable_until',
                       'status',
                       'last_pricing_date',
                       'last_calculated_price',
                       'last_calculated_tax')
        }),
    )

    allow_add = False
