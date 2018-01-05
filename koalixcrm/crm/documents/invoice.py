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
from koalixcrm.crm.documents.salescontract import SalesContract
from koalixcrm.crm.documents.salescontract import TextParagraphInSalesContract
from koalixcrm.crm.documents.salescontractposition import SalesContractPosition
from koalixcrm.djangoUserExtension.models import TextParagraphInDocumentTemplate
from koalixcrm.crm.documents.pdfexport import PDFExport
from koalixcrm.plugin import *
from koalixcrm.crm.views import export_pdf
from koalixcrm.crm.documents.salescontract import SalesContractTextParagraph
from koalixcrm.crm.documents.salescontract import SalesContractPostalAddress
from koalixcrm.crm.documents.salescontract import SalesContractPhoneAddress
from koalixcrm.crm.documents.salescontract import SalesContractEmailAddress
from koalixcrm.crm.documents.salescontractposition import SalesContractInlinePosition
from koalixcrm.accounting.admin import InlineBookings
from koalixcrm.accounting.models import Account
import koalixcrm.crm.documents.contract
import koalixcrm.crm.documents.quote


class Invoice(SalesContract):
    payable_until = models.DateField(verbose_name=_("To pay until"))
    derived_from_quote = models.ForeignKey("Quote", blank=True, null=True)
    payment_bank_reference = models.CharField(verbose_name=_("Payment Bank Reference"), max_length=100, blank=True,
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
            self.customer = calling_model.default_customer
            self.currency = calling_model.default_currency
            self.description = calling_model.description
            self.template_set = calling_model.default_template_set.invoice_template
            self.discount = 0
        elif type(calling_model) == koalixcrm.crm.documents.quote.Quote:
            self.derived_from_quote = calling_model
            self.copy_sales_contract(calling_model)

        self.status = 'C'
        self.payable_until = date.today() + \
                             timedelta(days=self.customer.defaultCustomerBillingCycle.timeToPaymentDate)
        self.date_of_creation = date.today().__str__()
        self.save()

        if type(calling_model) == koalixcrm.crm.documents.contract.Contract:
            invoice_template = calling_model.default_template_set.invoice_template
            default_paragraphs = TextParagraphInDocumentTemplate.objects.filter(document_template=invoice_template)
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

        if self.last_pricing_date and self.last_calculated_price:
            return True
        else:
            return False

    def registerinvoiceinaccounting(self, request):
        dict_prices = dict()
        dict_tax = dict()
        currentValidAccountingPeriod = accounting.models.AccountingPeriod.getCurrentValidAccountingPeriod()
        activaaccount = accounting.models.Account.objects.filter(isopeninterestaccount=True)
        if not self.is_complete_with_price():
            raise IncompleteInvoice(_("Complete invoice and run price recalculation. Price may not be Zero"))
        if len(activaaccount) == 0:
            raise OpenInterestAccountMissing(_("Please specify one open intrest account in the accounting"))
        for position in list(SalesContractPosition.objects.filter(contract=self.id)):
            profitaccount = position.product.accoutingProductCategorie.profitAccount
            dict_prices[profitaccount] = position.lastCalculatedPrice
            dict_tax[profitaccount] = position.lastCalculatedTax

        for booking in accounting.models.Booking.objects.filter(accountingPeriod=currentValidAccountingPeriod):
            if booking.bookingReference == self:
                raise InvoiceAlreadyRegistered()
        for profitaccount, amount in iter(dict_prices.items()):
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
        booking.amount = self.last_calculated_price
        booking.staff = request.user
        booking.lastmodifiedby = request.user
        booking.save()

    def create_pdf(self):
        self.last_print_date = datetime.now()
        self.save()
        return PDFExport.create_pdf(self)

    def __str__(self):
        return _("Invoice") + ": " + str(self.id) + " " + _("from Contract") + ": " + str(self.contract.id)

    class Meta:
        app_label = "crm"
        verbose_name = _('Invoice')
        verbose_name_plural = _('Invoices')


class OptionInvoice(admin.ModelAdmin):
    list_display = (
    'id', 'description', 'contract', 'customer', 'payable_until', 'status', 'currency', 'staff',
    'last_calculated_price', 'last_calculated_tax', 'last_pricing_date', 'last_modification', 'last_modified_by', 'last_print_date')
    list_display_links = ('id', )
    list_filter = ('customer', 'contract', 'staff', 'status', 'currency', 'last_modification')
    ordering = ('id',)
    search_fields = ('contract__id', 'customer__name', 'currency__description')
    fieldsets = (
        (_('Basics'), {
            'fields': ('contract', 'description', 'customer', 'currency', 'discount',  'payable_until', 'status', 'external_reference', 'template_set' )
        }),
    )
    save_as = True
    inlines = [SalesContractInlinePosition, SalesContractTextParagraph, SalesContractPostalAddress, SalesContractPhoneAddress,
               SalesContractEmailAddress, InlineBookings]
    pluginProcessor = PluginProcessor()
    inlines.extend(pluginProcessor.getPluginAdditions("invoiceInlines"))

    class PaymentForm(forms.Form):
        paymentAmount = forms.DecimalField()
        _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
        paymentAccount = forms.ModelChoiceField(Account.objects.filter(accountType="A"))

    def response_add(self, request, obj, post_url_continue=None):
        new_obj = self.after_saving_model_and_related_inlines(request, obj)
        return super(OptionInvoice, self).response_add(request, new_obj)

    def response_change(self, request, obj):
        new_obj = self.after_saving_model_and_related_inlines(request, obj)
        return super(OptionInvoice, self).response_add(request, new_obj)

    def after_saving_model_and_related_inlines(self, request, obj):
        try:
            Calculations.calculate_document_price(obj, date.today())
            self.message_user(request, "Successfully calculated Prices")
        except Product.NoPriceFound as e:
            self.message_user(request, "Unsuccessfull in updating the Prices " + e.__str__(), level=messages.ERROR)
        return obj

    def save_model(self, request, obj, form, change):
        if (change == True):
            obj.last_modified_by = request.user
        else:
            obj.last_modified_by = request.user
            obj.staff = request.user
        obj.save()

    def recalculate_prices(self, request, queryset):
        for obj in queryset:
            self.after_saving_model_and_related_inlines(request, obj)
        return;

    recalculate_prices.short_description = _("Recalculate Prices")

    def create_pdf(self, request, queryset):
        for obj in queryset:
            response = export_pdf(self, request, obj, "/admin/crm/invoice/")
            return response

    create_pdf.short_description = _("Create PDF of Invoice")

    def registerInvoiceInAccounting(self, request, queryset):
        try:
            for obj in queryset:
                obj.registerinvoiceinaccounting(request)
            self.message_user(request, _("Successfully registered Invoice in the Accounting"))
            return;
        except OpenInterestAccountMissing as e:
            self.message_user(request, "Did not register Invoice in Accounting: " + e.__str__(), level=messages.ERROR)
            return;
        except IncompleteInvoice as e:
            self.message_user(request, "Did not register Invoice in Accounting: " + e.__str__(), level=messages.ERROR)
            return;

    registerInvoiceInAccounting.short_description = _("Register Invoice in Accounting")

    # def unregisterInvoiceInAccounting(self, request, queryset):
    # for obj in queryset:
    # obj.createPDF(deliveryorder=True)
    # self.message_user(request, _("Successfully unregistered Invoice in the Accounting"))
    # unregisterInvoiceInAccounting.short_description = _("Unregister Invoice in Accounting")

    def registerPaymentInAccounting(self, request, queryset):
        form = None
        if request.POST.get('post'):
            if 'cancel' in request.POST:
                self.message_user(request, _("Canceled registeration of payment in the accounting"), level=messages.ERROR)
                return
            elif 'register' in request.POST:
                form = self.PaymentForm(request.POST)
                if form.is_valid():
                    paymentAmount = form.cleaned_data['paymentAmount']
                    paymentAccount = form.cleaned_data['paymentAccount']
                    for obj in queryset:
                        obj.registerpaymentinaccounting(request, paymentAmount, paymentAccount)
                    self.message_user(request, _("Successfully registered Payment in the Accounting"))
                    return HttpResponseRedirect(request.get_full_path())
        else:
            form = self.PaymentForm
            c = {'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME, 'queryset': queryset, 'form': form}
            c.update(csrf(request))
            return render(request, 'crm/admin/registerPayment.html', c)


    registerPaymentInAccounting.short_description = _("Register Payment in Accounting")

    actions = ['recalculate_prices', 'create_pdf', 'registerInvoiceInAccounting',
               'unregisterInvoiceInAccounting', 'registerPaymentInAccounting',]
    pluginProcessor = PluginProcessor()
    actions.extend(pluginProcessor.getPluginAdditions("invoiceActions"))


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
