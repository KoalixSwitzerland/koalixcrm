# -*- coding: utf-8 -*-
from django import forms
from django.contrib import admin
from django.contrib import messages
from django.contrib.admin import helpers
from django.shortcuts import render
from django.template.context_processors import csrf
from django.utils.translation import ugettext as _
from koalixcrm.plugin import *

from apps.accounting.models import Account
from apps.accounting.models import Booking
from apps.crm.exceptions import *
from apps.crm.views import *


class ContractPostalAddress(admin.StackedInline):
    model = PostalAddressForContract
    extra = 1
    classes = ['collapse']
    fieldsets = (
        ('Basics', {
            'fields': (
            'prefix', 'prename', 'name', 'addressline1', 'addressline2', 'addressline3', 'addressline4', 'zipcode',
            'town', 'state', 'country', 'purpose'),
        }),
    )
    allow_add = True


class ContractPhoneAddress(admin.TabularInline):
    model = PhoneAddressForContract
    extra = 1
    classes = ['collapse']
    fieldsets = (
        ('Basics', {
            'fields': ('phone', 'purpose',)
        }),
    )
    allow_add = True


class ContractEmailAddress(admin.TabularInline):
    model = EmailAddressForContract
    extra = 1
    classes = ['collapse']
    fieldsets = (
        ('Basics', {
            'fields': ('email', 'purpose',)
        }),
    )
    allow_add = True


class PurchaseOrderPostalAddress(admin.StackedInline):
    model = PostalAddressForPurchaseOrder
    extra = 1
    classes = ['collapse']
    fieldsets = (
        ('Basics', {
            'fields': (
            'prefix', 'prename', 'name', 'addressline1', 'addressline2', 'addressline3', 'addressline4', 'zipcode',
            'town', 'state', 'country', 'purpose')
        }),
    )
    allow_add = True


class PurchaseOrderPhoneAddress(admin.TabularInline):
    model = PhoneAddressForPurchaseOrder
    extra = 1
    classes = ['collapse']
    fieldsets = (
        ('Basics', {
            'fields': ('phone', 'purpose',)
        }),
    )
    allow_add = True


class PurchaseOrderEmailAddress(admin.TabularInline):
    model = EmailAddressForPurchaseOrder
    extra = 1
    classes = ['collapse']
    fieldsets = (
        ('Basics', {
            'fields': ('email', 'purpose',)
        }),
    )
    allow_add = True


class SalesContractPostalAddress(admin.StackedInline):
    model = PostalAddressForSalesContract
    extra = 1
    classes = ['collapse']
    fieldsets = (
        ('Basics', {
            'fields': (
            'prefix', 'prename', 'name', 'addressline1', 'addressline2', 'addressline3', 'addressline4', 'zipcode',
            'town', 'state', 'country', 'purpose')
        }),
    )
    allow_add = True


class SalesContractPhoneAddress(admin.TabularInline):
    model = PhoneAddressForSalesContract
    extra = 1
    classes = ['collapse']
    fieldsets = (
        ('Basics', {
            'fields': ('phone', 'purpose',)
        }),
    )
    allow_add = True


class SalesContractEmailAddress(admin.TabularInline):
    model = EmailAddressForSalesContract
    extra = 1
    classes = ['collapse']
    fieldsets = (
        ('Basics', {
            'fields': ('email', 'purpose',)
        }),
    )
    allow_add = True


class SalesContractInlinePosition(admin.TabularInline):
    model = SalesContractPosition
    extra = 1
    classes = ['collapse']
    fieldsets = (
        ('', {
            'fields': (
            'positionNumber', 'quantity', 'unit', 'product', 'description', 'discount', 'overwriteProductPrice',
            'positionPricePerUnit', 'sentOn', 'supplier')
        }),
    )
    allow_add = True


class InlineQuote(admin.TabularInline):
    model = Quote
    classes = ['collapse']
    show_change_link = True
    can_delete = True
    extra = 1
    readonly_fields = (
    'description', 'contract', 'customer', 'validuntil', 'status', 'lastPricingDate', 'lastCalculatedPrice',
    'lastCalculatedTax',)
    fieldsets = (
        (_('Basics'), {
            'fields': ('description', 'contract', 'customer', 'validuntil', 'status')
        }),
        (_('Advanced (not editable)'), {
            'classes': ('collapse',),
            'fields': ('lastPricingDate', 'lastCalculatedPrice', 'lastCalculatedTax',)
        }),
    )
    allow_add = False


class InlineInvoice(admin.TabularInline):
    model = Invoice
    classes = ['collapse']
    show_change_link = True
    can_delete = True
    extra = 1
    readonly_fields = (
    'lastPricingDate', 'lastCalculatedPrice', 'lastCalculatedTax', 'description', 'contract', 'customer',
    'payableuntil', 'status')
    fieldsets = (
        (_('Basics'), {
            'fields': ('description', 'contract', 'customer', 'payableuntil', 'status'),
        }),
        (_('Advanced (not editable)'), {
            'classes': ('collapse',),
            'fields': ('lastPricingDate', 'lastCalculatedPrice', 'lastCalculatedTax',)
        }),
    )

    allow_add = False


class InlinePurchaseOrder(admin.TabularInline):
    model = PurchaseOrder
    classes = ['collapse']
    show_change_link = True
    can_delete = True
    extra = 1
    readonly_fields = (
    'description', 'contract', 'supplier', 'externalReference', 'status', 'lastPricingDate', 'lastCalculatedPrice')
    fieldsets = (
        (_('Basics'), {
            'fields': ('description', 'contract', 'supplier', 'externalReference', 'status')
        }),
        (_('Advanced (not editable)'), {
            'classes': ('collapse',),
            'fields': ('lastPricingDate', 'lastCalculatedPrice')
        }),
    )
    allow_add = False


class OptionContract(admin.ModelAdmin):
    list_display = ('id', 'description', 'defaultcustomer', 'defaultSupplier', 'staff', 'defaultcurrency')
    list_display_links = ('id', 'description', 'defaultcustomer', 'defaultSupplier', 'defaultcurrency')
    list_filter = ('defaultcustomer', 'defaultSupplier', 'staff', 'defaultcurrency')
    ordering = ('id', 'defaultcustomer', 'defaultcurrency')
    search_fields = ('id', 'contract', 'defaultcurrency__description')
    fieldsets = (
        (_('Basics'), {
            'fields': ('description', 'defaultcustomer', 'staff', 'defaultSupplier', 'defaultcurrency')
        }),
    )
    inlines = [ContractPostalAddress, ContractPhoneAddress, ContractEmailAddress, InlineQuote, InlineInvoice,
               InlinePurchaseOrder]
    pluginProcessor = PluginProcessor()
    inlines.extend(pluginProcessor.getPluginAdditions("contractInlines"))

    def createPurchaseOrder(self, request, queryset):
        for obj in queryset:
            purchaseorder = obj.createPurchaseOrder()
            self.message_user(request, _("PurchaseOrder created"))
            response = HttpResponseRedirect('/admin/crm/purchaseorder/' + str(purchaseorder.id))
        return response

    createPurchaseOrder.short_description = _("Create Purchaseorder")

    def createQuote(self, request, queryset):
        for obj in queryset:
            quote = obj.createQuote()
            self.message_user(request, _("Quote created"))
            response = HttpResponseRedirect('/admin/crm/quote/' + str(quote.id))
        return response

    createQuote.short_description = _("Create Quote")

    def createInvoice(self, request, queryset):
        for obj in queryset:
            invoice = obj.createInvoice()
            self.message_user(request, _("Invoice created"))
            response = HttpResponseRedirect('/admin/crm/invoice/' + str(invoice.id))
        return response

    createInvoice.short_description = _("Create Invoice")

    def save_model(self, request, obj, form, change):
        if (change == True):
            obj.lastmodifiedby = request.user
        else:
            obj.lastmodifiedby = request.user
            obj.staff = request.user
        obj.save()

    actions = ['createQuote', 'createInvoice', 'createPurchaseOrder']
    pluginProcessor = PluginProcessor()
    actions.extend(pluginProcessor.getPluginAdditions("contractActions"))


class PurchaseOrderInlinePosition(admin.TabularInline):
    model = PurchaseOrderPosition
    extra = 1
    classes = ['collapse']
    fieldsets = (
        ('', {
            'fields': (
            'positionNumber', 'quantity', 'unit', 'product', 'description', 'discount', 'overwriteProductPrice',
            'positionPricePerUnit', 'sentOn', 'supplier')
        }),
    )
    allow_add = True


class InlineBookings(admin.TabularInline):
    model = Booking
    extra = 1
    classes = ['collapse']
    fieldsets = (
        ('Basics', {
            'fields': ('fromAccount', 'toAccount', 'description', 'amount', 'bookingDate', 'staff', 'bookingReference',)
        }),
    )
    allow_add = False


class OptionInvoice(admin.ModelAdmin):
    list_display = (
    'id', 'description', 'contract', 'customer', 'payableuntil', 'status', 'currency', 'staff', 'lastCalculatedPrice',
    'lastPricingDate', 'lastmodification', 'lastmodifiedby')
    list_display_links = ('id', 'contract', 'customer')
    list_filter = ('customer', 'contract', 'staff', 'status', 'currency', 'lastmodification')
    ordering = ('contract', 'customer', 'currency')
    search_fields = ('contract__id', 'customer__name', 'currency__description')
    fieldsets = (
        (_('Basics'), {
            'fields': ('contract', 'description', 'customer', 'currency', 'discount',  'payableuntil', 'status')
        }),
    )
    save_as = True
    inlines = [SalesContractInlinePosition, SalesContractPostalAddress, SalesContractPhoneAddress,
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
            obj.recalculatePrices(date.today())
            self.message_user(request, "Successfully calculated Prices")
        except Product.NoPriceFound as e:
            self.message_user(request, "Unsuccessfull in updating the Prices " + e.__str__(), level=messages.ERROR)
        return obj

    def save_model(self, request, obj, form, change):
        if (change == True):
            obj.lastmodifiedby = request.user
        else:
            obj.lastmodifiedby = request.user
            obj.staff = request.user
        obj.save()

    def recalculatePrices(self, request, queryset):
        try:
            for obj in queryset:
                obj.recalculatePrices(date.today())
            self.message_user(request, "Successfully recalculated Prices")
        except Product.NoPriceFound as e:
            self.message_user(request, "Unsuccessfull in updating the Prices " + e.__str__(), level=messages.ERROR)
            return;

    recalculatePrices.short_description = _("Recalculate Prices")

    def createInvoicePDF(self, request, queryset):
        for obj in queryset:
            response = exportPDF(self, request, obj, "invoice", "/admin/crm/invoice/")
            return response

    createInvoicePDF.short_description = _("Create PDF of Invoice")

    def createDeliveryOrderPDF(self, request, queryset):
        for obj in queryset:
            response = exportPDF(self, request, obj, "deliveryorder", "/admin/crm/invoice/")
            return response

    createDeliveryOrderPDF.short_description = _("Create PDF of Delivery Order")

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

    actions = ['recalculatePrices', 'createDeliveryOrderPDF', 'createInvoicePDF', 'registerInvoiceInAccounting',
               'unregisterInvoiceInAccounting', 'registerPaymentInAccounting']
    pluginProcessor = PluginProcessor()
    actions.extend(pluginProcessor.getPluginAdditions("invoiceActions"))


class OptionQuote(admin.ModelAdmin):
    list_display = (
    'id', 'description', 'contract', 'customer', 'currency', 'validuntil', 'status', 'staff', 'lastmodifiedby',
    'lastCalculatedPrice', 'lastPricingDate', 'lastmodification')
    list_display_links = ('id', 'contract', 'customer', 'currency')
    list_filter = ('customer', 'contract', 'currency', 'staff', 'status', 'lastmodification')
    ordering = ('contract', 'customer', 'currency')
    search_fields = ('contract__id', 'customer__name', 'currency__description')

    fieldsets = (
        (_('Basics'), {
            'fields': ('contract', 'description', 'customer', 'currency', 'discount', 'validuntil', 'staff', 'status')
        }),
    )
    save_as = True
    inlines = [SalesContractInlinePosition, SalesContractPostalAddress, SalesContractPhoneAddress,
               SalesContractEmailAddress]
    pluginProcessor = PluginProcessor()
    inlines.extend(pluginProcessor.getPluginAdditions("quoteInlines"))

    def response_add(self, request, new_object):
        obj = self.after_saving_model_and_related_inlines(request, new_object)
        return super(OptionQuote, self).response_add(request, obj)

    def response_change(self, request, new_object):
        obj = self.after_saving_model_and_related_inlines(request, new_object)
        return super(OptionQuote, self).response_change(request, obj)

    def after_saving_model_and_related_inlines(self, request, obj):
        try:
            obj.recalculatePrices(date.today())
            self.message_user(request, "Successfully calculated Prices")
        except Product.NoPriceFound as e:
            self.message_user(request, "Unsuccessfull in updating the Prices " + e.__str__(), level=messages.ERROR)
        return obj

    def save_model(self, request, obj, form, change):
        if (change == True):
            obj.lastmodifiedby = request.user
        else:
            obj.lastmodifiedby = request.user
            obj.staff = request.user
        obj.save()

    def recalculatePrices(self, request, queryset):
        for obj in queryset:
            self.after_saving_model_and_related_inlines(request, obj)
        return;

    recalculatePrices.short_description = _("Recalculate Prices")

    def createInvoice(self, request, queryset):
        for obj in queryset:
            invoice = obj.createInvoice()
            self.message_user(request, _("Invoice created"))
            response = HttpResponseRedirect('/admin/crm/invoice/' + str(invoice.id))
        return response

    createInvoice.short_description = _("Create Invoice")

    def createQuotePDF(self, request, queryset):
        for obj in queryset:
            response = exportPDF(self, request, obj, "quote", "/admin/crm/quote/")
            return response

    createQuotePDF.short_description = _("Create PDF of Quote")

    def createPurchaseConfirmationPDF(self, request, queryset):
        for obj in queryset:
            response = exportPDF(self, request, obj, "purchaseconfirmation", "/admin/crm/quote/")
            return response

    createPurchaseConfirmationPDF.short_description = _("Create PDF of Purchase Confirmation")

    actions = ['recalculatePrices', 'createInvoice', 'createQuotePDF', 'createPurchaseConfirmationPDF']
    pluginProcessor = PluginProcessor()
    inlines.extend(pluginProcessor.getPluginAdditions("quoteActions"))


class OptionPurchaseOrder(admin.ModelAdmin):
    list_display = (
    'id', 'description', 'contract', 'supplier', 'status', 'currency', 'staff', 'lastmodifiedby', 'lastCalculatedPrice',
    'lastPricingDate', 'lastmodification')
    list_display_links = ('id', 'contract', 'supplier',)
    list_filter = ('supplier', 'contract', 'staff', 'status', 'currency', 'lastmodification')
    ordering = ('contract', 'supplier', 'currency')
    search_fields = ('contract__id', 'supplier__name', 'currency_description')

    fieldsets = (
        (_('Basics'), {
            'fields': ('contract', 'description', 'supplier', 'currency', 'discount', 'status')
        }),
    )

    def save_model(self, request, obj, form, change):
        if (change == True):
            obj.lastmodifiedby = request.user
        else:
            obj.lastmodifiedby = request.user
            obj.staff = request.user
        obj.save()

    def createPurchseOrderPDF(self, request, queryset):
        for obj in queryset:
            response = exportPDF(self, request, obj, "purchaseorder", "/admin/crm/purchaseorder/")
            return response

    createPurchseOrderPDF.short_description = _("Create PDF of Purchase Order")

    actions = ['createPurchseOrderPDF']
    pluginProcessor = PluginProcessor()
    actions.extend(pluginProcessor.getPluginAdditions("purchaseOrderActions"))

    save_as = True
    inlines = [PurchaseOrderInlinePosition, PurchaseOrderPostalAddress, PurchaseOrderPhoneAddress,
               PurchaseOrderEmailAddress]
    pluginProcessor = PluginProcessor()
    inlines.extend(pluginProcessor.getPluginAdditions("purchaseOrderInlines"))


class ProductPrice(admin.TabularInline):
    model = Price
    extra = 1
    classes = ['collapse']
    fieldsets = (
        ('', {
            'fields': ('price', 'validfrom', 'validuntil', 'unit', 'customerGroup', 'currency')
        }),
    )
    allow_add = True


class ProductUnitTransform(admin.TabularInline):
    model = UnitTransform
    extra = 1
    classes = ['collapse']
    fieldsets = (
        ('', {
            'fields': ('fromUnit', 'toUnit', 'factor',)
        }),
    )
    allow_add = True


class OptionProduct(admin.ModelAdmin):
    list_display = ('productNumber', 'title', 'defaultunit', 'tax', 'accoutingProductCategorie')
    list_display_links = ('productNumber',)
    fieldsets = (
        (_('Basics'), {
            'fields': ('productNumber', 'title', 'description', 'defaultunit', 'tax', 'accoutingProductCategorie')
        }),)
    inlines = [ProductPrice, ProductUnitTransform]


class ContactPostalAddress(admin.StackedInline):
    model = PostalAddressForContact
    extra = 1
    classes = ['collapse']
    fieldsets = (
        ('Basics', {
            'fields': (
            'prefix', 'prename', 'name', 'addressline1', 'addressline2', 'addressline3', 'addressline4', 'zipcode',
            'town', 'state', 'country', 'purpose')
        }),
    )
    allow_add = True


class ContactPhoneAddress(admin.TabularInline):
    model = PhoneAddressForContact
    extra = 1
    classes = ['collapse']
    fieldsets = (
        ('Basics', {
            'fields': ('phone', 'purpose',)
        }),
    )
    allow_add = True


class ContactEmailAddress(admin.TabularInline):
    model = EmailAddressForContact
    extra = 1
    classes = ['collapse']
    fieldsets = (
        ('Basics', {
            'fields': ('email', 'purpose',)
        }),
    )
    allow_add = True


class OptionCustomer(admin.ModelAdmin):
    list_display = ('id', 'name', 'defaultCustomerBillingCycle',)
    fieldsets = (('', {'fields': ('name', 'defaultCustomerBillingCycle', 'ismemberof',)}),)
    allow_add = True
    ordering = ('id', 'name')
    search_fields = ('id', 'name')
    inlines = [ContactPostalAddress, ContactPhoneAddress, ContactEmailAddress]
    pluginProcessor = PluginProcessor()
    inlines.extend(pluginProcessor.getPluginAdditions("customerInline"))

    @staticmethod
    def createContract(request, queryset):
        for obj in queryset:
            contract = obj.createContract(request)
            response = HttpResponseRedirect('/admin/crm/contract/' + str(contract.id))
        return response

    createContract.short_description = _("Create Contract")

    @staticmethod
    def createQuote(queryset):
        for obj in queryset:
            quote = obj.createQuote()
            response = HttpResponseRedirect('/admin/crm/quote/' + str(quote.id))
        return response

    createQuote.short_description = _("Create Quote")

    @staticmethod
    def createInvoice(queryset):
        for obj in queryset:
            invoice = obj.createInvoice()
            response = HttpResponseRedirect('/admin/crm/invoice/' + str(invoice.id))
        return response

    createInvoice.short_description = _("Create Invoice")

    def save_model(self, request, obj, form, change):
        if (change == True):
            obj.lastmodifiedby = request.user
        else:
            obj.lastmodifiedby = request.user
            obj.staff = request.user
        obj.save()

    actions = ['createContract', 'createInvoice', 'createQuote']
    pluginProcessor = PluginProcessor()
    inlines.extend(pluginProcessor.getPluginAdditions("customerActions"))


class OptionCustomerGroup(admin.ModelAdmin):
    list_display = ('id', 'name')
    fieldsets = (('', {'fields': ('name',)}),)
    allow_add = True


class OptionSupplier(admin.ModelAdmin):
    list_display = ('id', 'name', 'offersShipmentToCustomers')
    fieldsets = (('', {'fields': ('name', 'offersShipmentToCustomers')}),)
    inlines = [ContactPostalAddress, ContactPhoneAddress, ContactEmailAddress]
    allow_add = True

    def save_model(self, request, obj, form, change):
        if (change == True):
            obj.lastmodifiedby = request.user
        else:
            obj.lastmodifiedby = request.user
            obj.staff = request.user
        obj.save()


class OptionUnit(admin.ModelAdmin):
    list_display = ('id', 'description', 'shortName', 'isAFractionOf', 'fractionFactorToNextHigherUnit')
    fieldsets = (('', {'fields': ('description', 'shortName', 'isAFractionOf', 'fractionFactorToNextHigherUnit')}),)
    allow_add = True


class OptionCurrency(admin.ModelAdmin):
    list_display = ('id', 'description', 'shortName', 'rounding')
    fieldsets = (('', {'fields': ('description', 'shortName', 'rounding')}),)
    allow_add = True


class OptionTax(admin.ModelAdmin):
    list_display = ('id', 'taxrate', 'name', 'accountActiva', 'accountPassiva')
    fieldsets = (('', {'fields': ('taxrate', 'name', 'accountActiva', 'accountPassiva')}),)
    allow_add = True


class OptionCustomerBillingCycle(admin.ModelAdmin):
    list_display = ('id', 'timeToPaymentDate', 'name')
    fieldsets = (('', {'fields': ('timeToPaymentDate', 'name',)}),)
    allow_add = True


admin.site.register(Customer, OptionCustomer)
admin.site.register(CustomerGroup, OptionCustomerGroup)
admin.site.register(Supplier, OptionSupplier)
admin.site.register(Quote, OptionQuote)
admin.site.register(Invoice, OptionInvoice)
admin.site.register(Unit, OptionUnit)
admin.site.register(Currency, OptionCurrency)
admin.site.register(Tax, OptionTax)
admin.site.register(CustomerBillingCycle, OptionCustomerBillingCycle)
admin.site.register(Contract, OptionContract)
admin.site.register(PurchaseOrder, OptionPurchaseOrder)
admin.site.register(Product, OptionProduct)
