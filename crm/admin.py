# -*- coding: utf-8 -*-
import os
from django import forms
from django.core.urlresolvers import reverse
from datetime import date
from crm.models import *
from django.utils.translation import ugettext as _
from django.contrib import admin
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.servers.basehttp import FileWrapper



   
class ContractPostalAddress(admin.StackedInline):
   model = PostalAddressForContract
   extra = 1
   classes = ('collapse-open',)
   fieldsets = (
      ('Basics', {
         'fields': ('prefix', 'prename', 'name', 'addressline1', 'addressline2', 'addressline3', 'addressline4', 'zipcode', 'town', 'state', 'country', 'purpose')
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
         'fields': ('prefix', 'prename', 'name', 'addressline1', 'addressline2', 'addressline3', 'addressline4', 'zipcode', 'town', 'state', 'country', 'purpose')
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
         'fields': ('prefix', 'prename', 'name', 'addressline1', 'addressline2', 'addressline3', 'addressline4', 'zipcode', 'town', 'state', 'country', 'purpose')
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
            'fields': ('positionNumber', 'quantity', 'unit', 'product', 'description', 'discount', 'overwriteProductPrice', 'positionPricePerUnit', 'sentOn', 'shipmentPartner')
        }),
    )
    allow_add = True


class InlineQuote(admin.TabularInline):
   model = Quote
   classes = ('collapse-open')
   extra = 1
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
   classes = ('collapse-open')
   extra = 1
   fieldsets = (
      (_('Basics'), {
         'fields': ('description', 'contract', 'customer', 'payableuntil', 'status')
      }),
      (_('Advanced (not editable)'), {
         'classes': ('collapse',),
         'fields': ('lastPricingDate', 'lastCalculatedPrice', 'lastCalculatedTax',)
      }),
   )
   allow_add = False
   
class InlinePurchaseOrder(admin.TabularInline):
   model = PurchaseOrder
   classes = ('collapse-open')
   extra = 1
   fieldsets = (
      (_('Basics'), {
         'fields': ('description', 'contract', 'distributor', 'externalReference', 'status')
      }),
      (_('Advanced (not editable)'), {
         'classes': ('collapse',),
         'fields': ('lastPricingDate', 'lastCalculatedPrice')
      }),
   )
   allow_add = False

class OptionContract(admin.ModelAdmin):
   list_display = ('id', 'description', 'defaultcustomer', 'defaultdistributor', 'staff', 'defaultcurrency')
   list_display_links = ('id','description', 'defaultcustomer', 'defaultdistributor', 'defaultcurrency')       
   list_filter    = ('defaultcustomer', 'defaultdistributor', 'staff', 'defaultcurrency')
   ordering       = ('id', 'defaultcustomer', 'defaultcurrency')
   search_fields  = ('id','contract', 'defaultcurrency__description')
   fieldsets = (
      (_('Basics'), {
         'fields': ('description', 'defaultcustomer', 'defaultdistributor', 'defaultcurrency')
      }),
   )
   inlines = [ContractPostalAddress, ContractPhoneAddress, ContractEmailAddress, InlineQuote, InlineInvoice, InlinePurchaseOrder]

   def createPurchaseOrder(self, request, queryset):
      for obj in queryset:
         purchaseorder = obj.createPurchaseOrder()
         self.message_user(request, _("PurchaseOrder created"))
         response = HttpResponseRedirect('/admin/crm/purchaseorder/'+str(purchaseorder.id))
      return response
   createPurchaseOrder.short_description = _("Create Purchaseorder")
   
   def createQuote(self, request, queryset):
      for obj in queryset:
         quote = obj.createQuote()
         self.message_user(request, _("Quote created"))
         response = HttpResponseRedirect('/admin/crm/quote/'+str(quote.id))
      return response
   createQuote.short_description = _("Create Quote")
   
   def createInvoice(self, request, queryset):
      for obj in queryset:
         invoice = obj.createInvoice()
         self.message_user(request, _("Invoice created"))
         response = HttpResponseRedirect('/admin/crm/invoice/'+str(invoice.id))
      return response
   createInvoice.short_description = _("Create Invoice")
    
   def save_model(self, request, obj, form, change):
      obj.staff = request.user
      obj.save()
      
   actions = ['createQuote', 'createInvoice', 'createPurchaseOrder']


class PurchaseOrderInlinePosition(admin.TabularInline):
    model = PurchaseOrderPosition
    extra = 1
    classes = ('collapse-open',)
    fieldsets = (
        ('', {
            'fields': ('positionNumber', 'quantity', 'unit', 'product', 'description', 'discount', 'overwriteProductPrice', 'positionPricePerUnit', 'sentOn', 'shipmentPartner')
        }),
    )
    allow_add = True


class OptionInvoice(admin.ModelAdmin):
   list_display = ('id', 'description', 'contract', 'customer', 'payableuntil', 'status', 'currency', 'staff',  'lastCalculatedPrice', 'lastPricingDate', 'lastmodification', 'lastmodifiedby')
   list_display_links = ('id','contract','customer')       
   list_filter    = ('customer', 'contract', 'staff', 'status', 'currency', 'lastmodification')
   ordering       = ('contract', 'customer', 'currency')
   search_fields  = ('contract__id', 'customer__name', 'currency__description')
   fieldsets = (
      (_('Basics'), {
         'fields': ('contract', 'description', 'customer', 'currency', 'payableuntil', 'status')
      }),
   )
   save_as = True
   inlines = [SalesContractInlinePosition, SalesContractPostalAddress, SalesContractPhoneAddress, SalesContractEmailAddress]

   def save_model(self, request, obj, form, change):
      obj.staff = request.user
      obj.save()
      
   def recalculatePrices(self, request, queryset):
     try:
        for obj in queryset:
            obj.recalculatePrices(date.today())
        self.message_user(request, "Successfully recalculated Prices")
     except Product.NoPriceFound as e : 
        self.message_user(request, "Unsuccessfull in updating the Prices "+ e.__str__())
        return;
   recalculatePrices.short_description = _("Recalculate Prices")
         
   def createInvoicePDF(self, request, queryset):
      for obj in queryset:
         response = HttpResponseRedirect('/export/invoice/'+str(obj.id))
         return response
   createInvoicePDF.short_description = _("Create PDF of Invoice")
   
   def createDeliveryOrderPDF(self, request, queryset):
      for obj in queryset:
         response = HttpResponseRedirect('/export/deilveryorder/'+str(obj.id))
         return response
   createDeliveryOrderPDF.short_description = _("Create PDF of Delivery Order")
         
   def registerInvoiceInAccounting(self, request, queryset):
      for obj in queryset:
         obj.registerinvoiceinaccounting(request)
         self.message_user(request, _("Successfully registered Invoice in the Accounting"))
   registerInvoiceInAccounting.short_description = _("Register Invoice in Accounting")
   
   def unregisterInvoiceInAccounting(self, request, queryset):
      for obj in queryset:
         obj.createPDF(deliveryorder=True)
         self.message_user(request, _("Successfully unregistered Invoice in the Accounting"))
   unregisterInvoiceInAccounting.short_description = _("Unregister Invoice in Accounting")
   
   def registerPaymentInAccounting(self, request, queryset):
      for obj in queryset:
         obj.registerpaymentinaccounting(request)
         self.message_user(request, _("Successfully registered Payment in the Accounting"))
   registerPaymentInAccounting.short_description = _("Register Payment in Accounting")
   
   actions = ['recalculatePrices', 'createDeliveryOrderPDF', 'createInvoicePDF', 'registerInvoiceInAccounting', 'unregisterInvoiceInAccounting', 'registerPaymentInAccounting']


class OptionQuote(admin.ModelAdmin):
   list_display = ('id', 'description', 'contract', 'customer', 'currency', 'validuntil', 'status', 'staff', 'lastmodifiedby', 'lastCalculatedPrice', 'lastPricingDate', 'lastmodification')
   list_display_links = ('id','contract','customer', 'currency')        
   list_filter    = ('customer', 'contract', 'currency', 'staff', 'status', 'lastmodification')
   ordering       = ('contract', 'customer', 'currency')
   search_fields  = ('contract__id', 'customer__name', 'currency__description')

   fieldsets = (
      (_('Basics'), {
         'fields': ('contract', 'description', 'customer', 'currency', 'validuntil', 'status')
      }),
   )
   save_as = True
   inlines = [SalesContractInlinePosition, SalesContractPostalAddress, SalesContractPhoneAddress, SalesContractEmailAddress]

   def save_model(self, request, obj, form, change):
      obj.staff = request.user
      obj.save()

   def recalculatePrices(self, request, queryset):
     try:
        for obj in queryset:
           obj.recalculatePrices(date.today())
           self.message_user(request, _("Successfully recalculated Prices"))
     except Product.NoPriceFound as e : 
        self.message_user(request, _("Unsuccessfull in updating the Prices ")+ e.__str__())
        return;
   recalculatePrices.short_description = _("Recalculate Prices")

   def createInvoice(self, request, queryset):
      for obj in queryset:
         invoice = obj.createInvoice()
         self.message_user(request, _("Invoice created"))
         response = HttpResponseRedirect('/admin/crm/invoice/'+str(invoice.id))
      return response
   createInvoice.short_description = _("Create Invoice")
         
   def createQuotePDF(self, request, queryset):
      for obj in queryset:
         response = HttpResponseRedirect('/export/quote/'+str(obj.id))
         return response
   createQuotePDF.short_description = _("Create PDF of Quote")
         
   def createPurchaseConfirmationPDF(self, request, queryset):
      for obj in queryset:
         response = HttpResponseRedirect('/export/purchaseconfirmation/'+str(obj.id))
         return response
   createPurchaseConfirmationPDF.short_description = _("Create PDF of Purchase Confirmation")

   actions = ['recalculatePrices', 'createInvoice', 'createQuotePDF', 'createPurchaseConfirmationPDF']

class OptionPurchaseOrder(admin.ModelAdmin):
   list_display = ('id', 'description', 'contract', 'distributor', 'status', 'currency', 'staff', 'lastmodifiedby', 'lastCalculatedPrice', 'lastPricingDate', 'lastmodification')
   list_display_links = ('id','contract','distributor', )        
   list_filter    = ('distributor', 'contract', 'staff', 'status', 'currency', 'lastmodification')
   ordering       = ('contract', 'distributor', 'currency')
   search_fields  = ('contract__id', 'distributor__name', 'currency_description')

   fieldsets = (
      (_('Basics'), {
         'fields': ('contract', 'description', 'distributor', 'currency', 'status')
      }),
   )
   
   def save_model(self, request, obj, form, change):
      obj.staff = request.user
      obj.save()
         
   def createPurchseOrderPDF(self, request, queryset):
      for obj in queryset:
         response = HttpResponseRedirect('/export/purchaseorder/'+str(obj.id))
         return response
   createPurchseOrderPDF.short_description = _("Create PDF of Purchase Order")
   
   actions = ['createPurchseOrderPDF']
   
   save_as = True
   inlines = [PurchaseOrderInlinePosition, PurchaseOrderPostalAddress, PurchaseOrderPhoneAddress, PurchaseOrderEmailAddress]

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
   list_display = ('productNumber', 'title','defaultunit', 'tax', 'accoutingProductCategorie')
   list_display_links = ('productNumber',)
   fieldsets = (
      (_('Basics'), {
         'fields': ('productNumber', 'title', 'description', 'defaultunit', 'tax', 'accoutingProductCategorie')
      }),)
   inlines = [ProductPrice, ProductUnitTransform]
   
class ContactPostalAddress(admin.StackedInline):
   model = PostalAddressForContact
   extra = 1
   classes = ('collapse-open',)
   fieldsets = (
      ('Basics', {
         'fields': ('prefix', 'prename', 'name', 'addressline1', 'addressline2', 'addressline3', 'addressline4', 'zipcode', 'town', 'state', 'country', 'purpose')
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
   list_display = ('id', 'name', 'defaultModeOfPayment', )
   fieldsets = (('', {'fields': ('name', 'defaultModeOfPayment', 'ismemberof',)}),)
   allow_add = True   
   ordering       = ('id', 'name')
   search_fields  = ('id', 'name')
   inlines = [ContactPostalAddress, ContactPhoneAddress, ContactEmailAddress]

   def createContract(self, request, queryset):
      for obj in queryset:
         contract = obj.createContract()
         response = HttpResponseRedirect('/admin/crm/contract/'+str(contract.id))
      return response
   createContract.short_description = _("Create Contract")
   
   def createQuote(self, request, queryset):
      for obj in queryset:
         quote = obj.createQuote()
         response = HttpResponseRedirect('/admin/crm/quote/'+str(quote.id))
      return response
   createQuote.short_description = _("Create Quote")
   
   def createInvoice(self, request, queryset):
      for obj in queryset:
         invoice = obj.createInvoice()
         response = HttpResponseRedirect('/admin/crm/invoice/'+str(invoice.id))
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

class OptionCustomerGroup(admin.ModelAdmin):
   list_display = ('id', 'name' )
   fieldsets = (('', {'fields': ('name',)}),)
   allow_add = True

class OptionDistributor(admin.ModelAdmin):
   list_display = ('id', 'name')
   fieldsets = (('', {'fields': ('name',)}),)
   inlines = [ContactPostalAddress, ContactPhoneAddress, ContactEmailAddress]
   allow_add = True
   
   def save_model(self, request, obj, form, change):
     if (change == True):
       obj.lastmodifiedby = request.user
     else:
       obj.lastmodifiedby = request.user
       obj.staff = request.user
     obj.save()


class OptionShipmentPartner(admin.ModelAdmin):
   list_display = ('id', 'name')
   fieldsets = (('', {'fields': ('name',)}),)
   inlines = [ContactPostalAddress, ContactPhoneAddress, ContactEmailAddress]
   allow_add = True
   
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
   
class OptionModeOfPayment(admin.ModelAdmin):
   list_display = ('id', 'timeToPaymentDate', 'name')
   fieldsets = (('', {'fields': ('timeToPaymentDate', 'name',)}),)
   allow_add = True

 
admin.site.register(Customer, OptionCustomer)
admin.site.register(CustomerGroup, OptionCustomerGroup)
admin.site.register(Distributor, OptionDistributor)
admin.site.register(ShipmentPartner, OptionShipmentPartner)
admin.site.register(Quote, OptionQuote)
admin.site.register(Invoice, OptionInvoice)
admin.site.register(Unit, OptionUnit)
admin.site.register(Currency, OptionCurrency)
admin.site.register(Tax, OptionTax)
admin.site.register(ModeOfPayment, OptionModeOfPayment)
admin.site.register(Contract, OptionContract)
admin.site.register(PurchaseOrder, OptionPurchaseOrder)
admin.site.register(Product, OptionProduct)
