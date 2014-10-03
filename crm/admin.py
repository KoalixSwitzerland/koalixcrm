# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.utils.translation import ugettext as trans
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.admin import helpers

from crm.views import *
from accounting.models import Booking
from KoalixCRM.plugin import *


class ContractPostalAddress(admin.StackedInline):
    model = PostalAddressForContract
    extra = 1
    classes = ('collapse-open',)
    fieldsets = (
        ('Basics', {
            'fields': (
                'prefix', 'prename', 'name', 'addressline1', 'addressline2', 'addressline3', 'addressline4', 'zipcode',
                'town', 'state', 'country', 'purpose')
        }),
    )
    allow_add = True


class ContractPhoneAddress(admin.TabularInline):
    model = PhoneAddressForContract
    extra = 1
    classes = ('collapse-open',)
    fieldsets = (
        ('Basics', {
            'fields': ('phone', 'purpose',)
        }),
    )
    allow_add = True


class ContractEmailAddress(admin.TabularInline):
    model = EmailAddressForContract
    extra = 1
    classes = ('collapse-open',)
    fieldsets = (
        ('Basics', {
            'fields': ('email', 'purpose',)
        }),
    )
    allow_add = True


class PurchaseOrderPostalAddress(admin.StackedInline):
    model = PostalAddressForPurchaseOrder
    extra = 1
    classes = ('collapse-open',)
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
    classes = ('collapse-open',)
    fieldsets = (
        ('Basics', {
            'fields': ('phone', 'purpose',)
        }),
    )
    allow_add = True


class PurchaseOrderEmailAddress(admin.TabularInline):
    model = EmailAddressForPurchaseOrder
    extra = 1
    classes = ('collapse-open',)
    fieldsets = (
        ('Basics', {
            'fields': ('email', 'purpose',)
        }),
    )
    allow_add = True


class SalesContractPostalAddress(admin.StackedInline):
    model = PostalAddressForSalesContract
    extra = 1
    classes = ('collapse-open',)
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
    classes = ('collapse-open',)
    fieldsets = (
        ('Basics', {
            'fields': ('phone', 'purpose',)
        }),
    )
    allow_add = True


class SalesContractEmailAddress(admin.TabularInline):
    model = EmailAddressForSalesContract
    extra = 1
    classes = ('collapse-open',)
    fieldsets = (
        ('Basics', {
            'fields': ('email', 'purpose',)
        }),
    )
    allow_add = True


class SalesContractInlinePosition(admin.TabularInline):
    model = SalesContractPosition
    extra = 1
    classes = ('collapse-open',)
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
    classes = ('collapse-open')
    extra = 1
    readonly_fields = (
        'description', 'contract', 'customer', 'validuntil', 'status', 'lastPricingDate', 'lastCalculatedPrice',
        'lastCalculatedTax', )
    fieldsets = (
        (trans('Basics'), {
            'fields': ('description', 'contract', 'customer', 'validuntil', 'status')
        }),
        (trans('Advanced (not editable)'), {
            'classes': ('collapse',),
            'fields': ('lastPricingDate', 'lastCalculatedPrice', 'lastCalculatedTax',)
        }),
    )
    allow_add = False


class InlineInvoice(admin.TabularInline):
    model = Invoice
    classes = ('collapse-open')
    extra = 1
    readonly_fields = (
        'lastPricingDate', 'lastCalculatedPrice', 'lastCalculatedTax', 'description', 'contract', 'customer',
        'payableuntil', 'status' )
    fieldsets = (
        (trans('Basics'), {
            'fields': ('description', 'contract', 'customer', 'payableuntil', 'status'),
        }),
        (trans('Advanced (not editable)'), {
            'classes': ('collapse',),
            'fields': ('lastPricingDate', 'lastCalculatedPrice', 'lastCalculatedTax',)
        }),
    )

    allow_add = False


class InlinePurchaseOrder(admin.TabularInline):
    model = PurchaseOrder
    classes = ('collapse-open')
    extra = 1
    readonly_fields = (
        'description', 'contract', 'supplier', 'externalReference', 'status', 'lastPricingDate', 'lastCalculatedPrice' )
    fieldsets = (
        (trans('Basics'), {
            'fields': ('description', 'contract', 'supplier', 'externalReference', 'status')
        }),
        (trans('Advanced (not editable)'), {
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
        (trans('Basics'), {
            'fields': ('description', 'defaultcustomer', 'staff', 'defaultSupplier', 'defaultcurrency')
        }),
    )
    inlines = [ContractPostalAddress, ContractPhoneAddress, ContractEmailAddress, InlineQuote, InlineInvoice,
               InlinePurchaseOrder]
    pluginProcessor = PluginProcessor()
    inlines.extend(pluginProcessor.get_plugin_additions("contractInlines"))

    def createPurchaseOrder(self, request, queryset):
        response = ""
        for obj in queryset:
            purchaseorder = obj.create_purchase_order()
            self.message_user(request, trans("PurchaseOrder created"))
            response = HttpResponseRedirect('/admin/crm/purchaseorder/' + str(purchaseorder.id))
        return response

    createPurchaseOrder.short_description = trans("Create Purchaseorder")

    def createQuote(self, request, queryset):
        response = ""
        for obj in queryset:
            quote = obj.create_quote()
            self.message_user(request, trans("Quote created"))
            response = HttpResponseRedirect('/admin/crm/quote/' + str(quote.id))
        return response

    createQuote.short_description = trans("Create Quote")

    def createInvoice(self, request, queryset):
        response = ""
        for obj in queryset:
            invoice = obj.create_invoice()
            self.message_user(request, trans("Invoice created"))
            response = HttpResponseRedirect('/admin/crm/invoice/' + str(invoice.id))
        return response

    createInvoice.short_description = trans("Create Invoice")

    def save_model(self, request, obj, form, change):
        if change:
            obj.lastmodifiedby = request.user
        else:
            obj.lastmodifiedby = request.user
            obj.staff = request.user
        obj.save()

    actions = ['create_quote', 'create_invoice', 'create_purchase_order']
    pluginProcessor = PluginProcessor()
    actions.extend(pluginProcessor.get_plugin_additions("contractActions"))


class PurchaseOrderInlinePosition(admin.TabularInline):
    model = PurchaseOrderPosition
    extra = 1
    classes = ('collapse-open',)
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
    classes = ('collapse-open',)
    fieldsets = (
        ('Basics', {
            'fields': ('fromAccount', 'toAccount', 'description', 'amount', 'bookingDate', 'staff', 'bookingReference',)
        }),
    )
    allow_add = False


class OptionInvoice(admin.ModelAdmin):
    list_display = (
        'id', 'description', 'contract', 'customer', 'payableuntil', 'status', 'currency', 'staff',
        'lastCalculatedPrice',
        'lastPricingDate', 'lastModification', 'lastModifiedBy')
    list_display_links = ('id', 'contract', 'customer')
    list_filter = ('customer', 'contract', 'staff', 'status', 'currency', 'lastModification')
    ordering = ('contract', 'customer', 'currency')
    search_fields = ('contract__id', 'customer__name', 'currency__description')
    fieldsets = (
        (trans('Basics'), {
            'fields': ('contract', 'description', 'customer', 'currency', 'payableuntil', 'status')
        }),
    )
    save_as = True
    inlines = [SalesContractInlinePosition, SalesContractPostalAddress, SalesContractPhoneAddress,
               SalesContractEmailAddress, InlineBookings]
    pluginProcessor = PluginProcessor()
    inlines.extend(pluginProcessor.get_plugin_additions("invoiceInlines"))

    def response_add(self, request, new_object, **kwargs):
        obj = self.after_saving_model_and_related_inlines(request, new_object)
        return super(OptionInvoice, self).response_add(request, obj)

    def response_change(self, request, new_object):
        obj = self.after_saving_model_and_related_inlines(request, new_object)
        return super(OptionInvoice, self).response_add(request, obj)

    def after_saving_model_and_related_inlines(self, request, obj):
        try:
            obj.recalculate_prices(date.today())
            self.message_user(request, "Successfully calculated Prices")
        except Product.NoPriceFound as e:
            self.message_user(request, "Unsuccessfull in updating the Prices " + e.__str__())
        return obj

    def save_model(self, request, obj, form, change):
        if change:
            obj.lastmodifiedby = request.user
        else:
            obj.lastmodifiedby = request.user
            obj.staff = request.user
        obj.save()

    def recalculate_prices(self, request, queryset):
        try:
            for obj in queryset:
                obj.recalculate_prices(date.today())
            self.message_user(request, "Successfully recalculated Prices")
        except Product.NoPriceFound as e:
            self.message_user(request, "Unsuccessfull in updating the Prices " + e.__str__())
            return;

    recalculate_prices.short_description = trans("Recalculate Prices")

    def create_invoice_pdf(self, request, queryset):
        for obj in queryset:
            response = export_pdf(self, request, obj, "invoice", "/admin/crm/invoice/")
            return response

    create_invoice_pdf.short_description = trans("Create PDF of Invoice")

    def create_delivery_order_pdf(self, request, queryset):
        for obj in queryset:
            response = export_pdf(self, request, obj, "deliveryorder", "/admin/crm/invoice/")
            return response

    create_delivery_order_pdf.short_description = trans("Create PDF of Delivery Order")

    def register_invoice_in_accounting(self, request, queryset):
        for obj in queryset:
            obj.register_invoice_in_accounting(request)
            self.message_user(request, trans("Successfully registered Invoice in the Accounting"))

    register_invoice_in_accounting.short_description = trans("Register Invoice in Accounting")

    # def unregisterInvoiceInAccounting(self, request, queryset):
    # for obj in queryset:
    #obj.create_pdf(deliveryorder=True)
    #self.message_user(request, trans("Successfully unregistered Invoice in the Accounting"))
    #unregisterInvoiceInAccounting.short_description = trans("Unregister Invoice in Accounting")

    def register_payment_in_accounting(self, request, queryset):
        form = None
        if request.POST.get('post'):
            if 'cancel' in request.POST:
                self.message_user(request, trans("Canceled registeration of payment in the accounting"))
                return
            elif 'register' in request.POST:
                form = self.SeriesForm(request.POST)
                if form.is_valid():
                    series = form.cleaned_data['series']
                    for x in queryset:
                        y = Link(series=series, comic=x)
                        y.save()
                    self.message_user(request, trans("Successfully registered Payment in the Accounting"))
                    return HttpResponseRedirect(request.get_full_path())
        else:
            c = {'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME, 'queryset': queryset, 'form': form,
                 'path': request.get_full_path()}
            c.update(csrf(request))
            return render_to_response('admin/crm/registerPayment.html', c, context_instance=RequestContext(request))

    register_payment_in_accounting.short_description = trans("Register Payment in Accounting")

    actions = ['recalculate_prices', 'create_delivery_order_pdf', 'create_invoice_pdf',
               'register_invoice_in_accounting',
               'unregisterInvoiceInAccounting', 'register_payment_in_accounting']
    pluginProcessor = PluginProcessor()
    actions.extend(pluginProcessor.get_plugin_additions("invoiceActions"))


class OptionQuote(admin.ModelAdmin):
    list_display = (
        'id', 'description', 'contract', 'customer', 'currency', 'validuntil', 'status', 'staff', 'lastModifiedBy',
        'lastCalculatedPrice', 'lastPricingDate', 'lastModification')
    list_display_links = ('id', 'contract', 'customer', 'currency')
    list_filter = ('customer', 'contract', 'currency', 'staff', 'status', 'lastModification')
    ordering = ('contract', 'customer', 'currency')
    search_fields = ('contract__id', 'customer__name', 'currency__description')

    fieldsets = (
        (trans('Basics'), {
            'fields': ('contract', 'description', 'customer', 'currency', 'validuntil', 'staff', 'status')
        }),
    )
    save_as = True
    inlines = [SalesContractInlinePosition, SalesContractPostalAddress, SalesContractPhoneAddress,
               SalesContractEmailAddress]
    pluginProcessor = PluginProcessor()
    inlines.extend(pluginProcessor.get_plugin_additions("quoteInlines"))

    def response_add(self, request, new_object, **kwargs):
        obj = self.after_saving_model_and_related_inlines(request, new_object)
        return super(OptionQuote, self).response_add(request, obj)

    def response_change(self, request, new_object):
        obj = self.after_saving_model_and_related_inlines(request, new_object)
        return super(OptionQuote, self).response_change(request, obj)

    def after_saving_model_and_related_inlines(self, request, obj):
        try:
            obj.recalculate_prices(date.today())
            self.message_user(request, "Successfully calculated Prices")
        except Product.NoPriceFound as e:
            self.message_user(request, "Unsuccessfull in updating the Prices " + e.__str__())
        return obj

    def save_model(self, request, obj, form, change):
        if change:
            obj.lastmodifiedby = request.user
        else:
            obj.lastmodifiedby = request.user
            obj.staff = request.user
        obj.save()

    def recalculate_prices(self, request, queryset):
        try:
            for obj in queryset:
                obj.recalculate_prices(date.today())
                self.message_user(request, trans("Successfully recalculated Prices"))
        except Product.NoPriceFound as e:
            self.message_user(request, trans("Unsuccessfull in updating the Prices ") + e.__str__())
            return

    recalculate_prices.short_description = trans("Recalculate Prices")

    def create_invoice(self, request, queryset):
        for obj in queryset:
            invoice = obj.create_invoice()
            self.message_user(request, trans("Invoice created"))
            response = HttpResponseRedirect('/admin/crm/invoice/' + str(invoice.id))
            return response

    create_invoice.short_description = trans("Create Invoice")

    def create_quote_pdf(self, request, queryset):
        for obj in queryset:
            response = export_pdf(self, request, obj, "quote", "/admin/crm/quote/")
            return response

    create_quote_pdf.short_description = trans("Create PDF of Quote")

    def create_purchase_confirmation_pdf(self, request, queryset):
        for obj in queryset:
            response = export_pdf(self, request, obj, "purchaseconfirmation", "/admin/crm/quote/")
            return response

    create_purchase_confirmation_pdf.short_description = trans("Create PDF of Purchase Confirmation")

    actions = ['recalculate_prices', 'create_invoice', 'create_quote_pdf', 'create_purchase_confirmation_pdf']
    pluginProcessor = PluginProcessor()
    inlines.extend(pluginProcessor.get_plugin_additions("quoteActions"))


class OptionPurchaseOrder(admin.ModelAdmin):
    list_display = (
        'id', 'description', 'contract', 'supplier', 'status', 'currency', 'staff', 'lastModifiedBy',
        'lastCalculatedPrice',
        'lastPricingDate', 'lastModification')
    list_display_links = ('id', 'contract', 'supplier', )
    list_filter = ('supplier', 'contract', 'staff', 'status', 'currency', 'lastModification')
    ordering = ('contract', 'supplier', 'currency')
    search_fields = ('contract__id', 'supplier__name', 'currency_description')

    fieldsets = (
        (trans('Basics'), {
            'fields': ('contract', 'description', 'supplier', 'currency', 'status')
        }),
    )

    def save_model(self, request, obj, form, change):
        if change:
            obj.lastmodifiedby = request.user
        else:
            obj.lastmodifiedby = request.user
            obj.staff = request.user
        obj.save()

    def create_purchase_order_pdf(self, request, queryset):
        for obj in queryset:
            response = export_pdf(self, request, obj, "purchaseorder", "/admin/crm/purchaseorder/")
            return response

    create_purchase_order_pdf.short_description = trans("Create PDF of Purchase Order")

    actions = ['create_purchase_order_pdf']
    pluginProcessor = PluginProcessor()
    actions.extend(pluginProcessor.get_plugin_additions("purchaseOrderActions"))

    save_as = True
    inlines = [PurchaseOrderInlinePosition, PurchaseOrderPostalAddress, PurchaseOrderPhoneAddress,
               PurchaseOrderEmailAddress]
    pluginProcessor = PluginProcessor()
    inlines.extend(pluginProcessor.get_plugin_additions("purchaseOrderInlines"))


class ProductPrice(admin.TabularInline):
    model = Price
    extra = 1
    classes = ('collapse-open',)
    fieldsets = (
        ('', {
            'fields': ('price', 'validfrom', 'validuntil', 'unit', 'customerGroup', 'currency')
        }),
    )
    allow_add = True


class ProductUnitTransform(admin.TabularInline):
    model = UnitTransform
    extra = 1
    classes = ('collapse-open',)
    fieldsets = (
        ('', {
            'fields': ('fromUnit', 'toUnit', 'factor', )
        }),
    )
    allow_add = True


class OptionProduct(admin.ModelAdmin):
    list_display = ('productNumber', 'title', 'defaultunit', 'tax', 'accoutingProductCategorie')
    list_display_links = ('productNumber',)
    fieldsets = (
        (trans('Basics'), {
            'fields': ('productNumber', 'title', 'description', 'defaultunit', 'tax', 'accoutingProductCategorie')
        }),)
    inlines = [ProductPrice, ProductUnitTransform]


class ContactPostalAddress(admin.StackedInline):
    model = PostalAddressForContact
    extra = 1
    classes = ('collapse-open',)
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
    classes = ('collapse-open',)
    fieldsets = (
        ('Basics', {
            'fields': ('phone', 'purpose',)
        }),
    )
    allow_add = True


class ContactEmailAddress(admin.TabularInline):
    model = EmailAddressForContact
    extra = 1
    classes = ('collapse-open',)
    fieldsets = (
        ('Basics', {
            'fields': ('email', 'purpose',)
        }),
    )
    allow_add = True


class OptionCustomer(admin.ModelAdmin):
    list_display = ('id', 'name', 'defaultCustomerBillingCycle', )
    fieldsets = (('', {'fields': ('name', 'defaultCustomerBillingCycle', 'ismemberof',)}),)
    allow_add = True
    ordering = ('id', 'name')
    search_fields = ('id', 'name')
    inlines = [ContactPostalAddress, ContactPhoneAddress, ContactEmailAddress]
    pluginProcessor = PluginProcessor()
    inlines.extend(pluginProcessor.get_plugin_additions("customerInline"))

    @staticmethod
    def create_contract(request, queryset):
        for obj in queryset:
            contract = obj.create_contract(request)
            response = HttpResponseRedirect('/admin/crm/contract/' + str(contract.id))
            return response

    create_contract.short_description = trans("Create Contract")

    @staticmethod
    def create_quote(request, queryset):
        for obj in queryset:
            quote = obj.create_quote()
            response = HttpResponseRedirect('/admin/crm/quote/' + str(quote.id))
            return response

    create_quote.short_description = trans("Create Quote")

    @staticmethod
    def create_invoice(request, queryset):
        for obj in queryset:
            invoice = obj.create_invoice()
            response = HttpResponseRedirect('/admin/crm/invoice/' + str(invoice.id))
            return response

    create_invoice.short_description = trans("Create Invoice")

    def save_model(self, request, obj, form, change):
        if change:
            obj.lastmodifiedby = request.user
        else:
            obj.lastmodifiedby = request.user
            obj.staff = request.user
        obj.save()

    actions = ['create_contract', 'create_invoice', 'create_quote']
    pluginProcessor = PluginProcessor()
    inlines.extend(pluginProcessor.get_plugin_additions("customerActions"))


class OptionCustomerGroup(admin.ModelAdmin):
    list_display = ('id', 'name' )
    fieldsets = (('', {'fields': ('name',)}),)
    allow_add = True


class OptionSupplier(admin.ModelAdmin):
    list_display = ('id', 'name')
    fieldsets = (('', {'fields': ('name',)}),)
    inlines = [ContactPostalAddress, ContactPhoneAddress, ContactEmailAddress]
    allow_add = True

    def save_model(self, request, obj, form, change):
        if change:
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
