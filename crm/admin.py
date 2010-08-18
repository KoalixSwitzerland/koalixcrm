# -*- coding: utf-8 -*-
from django import forms
from django.core.urlresolvers import reverse
from datetime import date
from crm.models import *
from django.utils.translation import ugettext as _
from django.contrib import admin

   
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
         'fields': ('description', 'contract', 'customer', 'validuntil', 'state')
      }),
      (_('Advanced (not editable)'), {
         'classes': ('collapse',),
         'fields': ('lastPricingDate', 'lastCalculatedPrice')
      }),
   )
   allow_add = True
   
   inlines = [SalesContractInlinePosition, SalesContractPostalAddress, SalesContractPhoneAddress, SalesContractEmailAddress]
   
class InlineInvoice(admin.TabularInline):
   model = Invoice
   classes = ('collapse-open')
   extra = 1
   fieldsets = (
      (_('Basics'), {
         'fields': ('description', 'contract', 'customer', 'payableuntil', 'state')
      }),
      (_('Advanced (not editable)'), {
         'classes': ('collapse',),
         'fields': ('lastPricingDate', 'lastCalculatedPrice')
      }),
   )
   allow_add = True
   
   inlines = [SalesContractInlinePosition, SalesContractPostalAddress, SalesContractPhoneAddress, SalesContractEmailAddress]

class OptionContract(admin.ModelAdmin):
   list_display = ('id', 'description', 'defaultcustomer', 'defaultdistributor', 'staff')
   list_display_links = ('id','description', 'defaultcustomer', 'defaultdistributor')       
   list_filter    = ('defaultcustomer', 'defaultdistributor', 'staff')
   ordering       = ('id', 'defaultcustomer')
   search_fields  = ('id','contract')
   fieldsets = (
      (_('Basics'), {
         'fields': ('description', 'defaultcustomer', 'defaultdistributor')
      }),
   )
   save_as = True
   inlines = [ContractPostalAddress, ContractPhoneAddress, ContractEmailAddress, InlineQuote, InlineInvoice]


class PurchaseOrderInlinePosition(admin.TabularInline):
    model = PurchaseOrderPosition
    extra = 1
    classes = ('collapse-open',)
    fieldsets = (
        ('', {
            'fields': ('positionNumber', 'quantity', 'product', 'description', 'discount', 'positionPricePerUnit', 'sentOn', 'shipmentPartner')
        }),
    )
    allow_add = True


class OptionInvoice(admin.ModelAdmin):
   list_display = ('id', 'description', 'contract', 'customer', 'payableuntil', 'state', 'staff', 'lastmodification', 'lastmodifiedby')
   list_display_links = ('id','contract','customer')       
   list_filter    = ('customer', 'contract', 'staff', 'state', 'lastmodification')
   ordering       = ('contract', 'customer')
   search_fields  = ('contract__id', 'customer__name')
   fieldsets = (
      (_('Basics'), {
         'fields': ('contract', 'description', 'customer', 'payableuntil', 'state')
      }),
      (_('Advanced (not editable)'), {
         'classes': ('collapse',),
         'fields': ('lastPricingDate', 'lastCalculatedPrice')
      }),
   )
   save_as = True
   inlines = [SalesContractInlinePosition, SalesContractPostalAddress, SalesContractPhoneAddress, SalesContractEmailAddress]

   def recalculatePrices(self, request, queryset):
     try:
        for obj in queryset:
            obj.recalculatePrices(date.today())
        self.message_user(request, "Successfully recalculated Prices")
     except Product.NoPriceFound as e : 
        self.message_user(request, "Unsuccessfull in updating the Prices "+ e.__str__())
        return;
   recalculatePrices.short_description = _("Recalculate Prices")
   actions = ['recalculatePrices']


class OptionQuote(admin.ModelAdmin):
   list_display = ('id', 'description', 'contract', 'customer', 'validuntil', 'state', 'staff', 'lastmodification', 'lastmodifiedby')
   list_display_links = ('id','contract','customer')        
   list_filter    = ('customer', 'contract', 'staff', 'state', 'lastmodification')
   ordering       = ('contract', 'customer')
   search_fields  = ('contract__id', 'customer__name')

   fieldsets = (
      (_('Basics'), {
         'fields': ('contract', 'description', 'customer', 'validuntil', 'state')
      }),
      (_('Advanced (not editable)'), {
         'classes': ('collapse',),
         'fields': ('lastPricingDate', 'lastCalculatedPrice')
      }),
   )
   save_as = True
   inlines = [SalesContractInlinePosition, SalesContractPostalAddress, SalesContractPhoneAddress, SalesContractEmailAddress]

   def recalculatePrices(self, request, queryset):
     try:
        for obj in queryset:
           obj.recalculatePrices(date.today())
           self.message_user(request, "Successfully recalculated Prices")
     except Product.NoPriceFound as e : 
        self.message_user(request, "Unsuccessfull in updating the Prices "+ e.__str__())
        return;
   recalculatePrices.short_description = _("Recalculate Prices")

   def createInvoice(self, request, queryset):
      for obj in queryset:
         obj.createInvoice()
   createInvoice.short_description = _("Create Invoice")
         
   def createPDF(sefl, request, queryset):
      for obj in queryset:
         obj.createPDF()
   createPDF.short_description = _("Create PDF")

   actions = ['recalculatePrices', 'createInvoice', 'createPDF']

class OptionPurchaseOrder(admin.ModelAdmin):
   list_display = ('distributor', 'state',)
   list_display_links = ('distributor', 'state')
   fieldsets = (
      (_('Basics'), {
         'fields': ('distributor', 'state', 'externalReference')
      }),
   )
   save_as = True
   inlines = [PurchaseOrderInlinePosition, PurchaseOrderPostalAddress, PurchaseOrderPhoneAddress, PurchaseOrderEmailAddress]

class ProductPrice(admin.TabularInline):
   model = Price
   extra = 1
   classes = ('collapse-open',)
   fieldsets = (
      ('', {
         'fields': ('price', 'validfrom', 'validuntil', 'unit', 'customerGroup')
      }),
   )
   allow_add = True

class OptionProduct(admin.ModelAdmin):
   list_display = ('productNumber', 'title','defaultunit', 'tax')
   list_display_links = ('productNumber',)
   fieldsets = (
      (_('Basics'), {
         'fields': ('productNumber', 'title', 'description', 'defaultunit', 'tax')
      }),)
   inlines = [ProductPrice]
   
class ContactPostalAddress(admin.StackedInline):
   model = PostalAddressForContact
   extra = 1
   classes = ('collapse-open',)
   fieldsets = (
      ('Basics', {
         'fields': ('prename', 'name', 'addressline1', 'addressline2', 'addressline3', 'addressline4', 'zipcode', 'town', 'state', 'country', 'purpose')
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
   list_display = ('id', 'name' )
   fieldsets = (('', {'fields': ('name',)}),)
   inlines = [ContactPostalAddress, ContactPhoneAddress, ContactEmailAddress]
   allow_add = True

class OptionCustomerGroup(admin.ModelAdmin):
   list_display = ('id', 'name' )
   fieldsets = (('', {'fields': ('name', 'member')}),)
   allow_add = True

class OptionDistributor(admin.ModelAdmin):
   list_display = ('id', 'name')
   fieldsets = (('', {'fields': ('name',)}),)
   inlines = [ContactPostalAddress, ContactPhoneAddress, ContactEmailAddress]
   allow_add = True


class OptionShipmentPartner(admin.ModelAdmin):
   list_display = ('id', 'name')
   fieldsets = (('', {'fields': ('name',)}),)
   inlines = [ContactPostalAddress, ContactPhoneAddress, ContactEmailAddress]
   allow_add = True
   
class OptionUnit(admin.ModelAdmin):
   list_display = ('id', 'description', 'shortName', 'isAFractionOf', 'fractionFactorToNextHigherUnit')
   fieldsets = (('', {'fields': ('description', 'shortName', 'isAFractionOf', 'fractionFactorToNextHigherUnit')}),)
   allow_add = True
   
class OptionTax(admin.ModelAdmin):
   list_display = ('id', 'taxrate', 'name')
   fieldsets = (('', {'fields': ('taxrate', 'name',)}),)
   allow_add = True


 
admin.site.register(Customer, OptionCustomer)
admin.site.register(CustomerGroup, OptionCustomerGroup)
admin.site.register(Distributor, OptionDistributor)
admin.site.register(ShipmentPartner, OptionShipmentPartner)
admin.site.register(Quote, OptionQuote)
admin.site.register(Invoice, OptionInvoice)
admin.site.register(Unit, OptionUnit)
admin.site.register(Tax, OptionTax)
admin.site.register(Contract, OptionContract)
admin.site.register(PurchaseOrder, OptionPurchaseOrder)
admin.site.register(Product, OptionProduct)
