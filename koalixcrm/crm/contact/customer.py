# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext as _
from koalixcrm.plugin import *
from koalixcrm import djangoUserExtension
from koalixcrm.crm.contact.contact import Contact, ContactCall, ContactVisit, PeopleInlineAdmin, PostalAddressForContact, ContactPostalAddress, ContactPhoneAddress, ContactEmailAddress, CityFilter, StateFilter
from koalixcrm.crm.contact.supplier import Supplier
from koalixcrm.crm.product.product import Product
from koalixcrm.crm.contact.person import *
from django.http import HttpResponseRedirect

import koalixcrm.crm.documents.contract

class Customer(Contact):
    defaultCustomerBillingCycle = models.ForeignKey('CustomerBillingCycle', verbose_name=_('Default Billing Cycle'))
    ismemberof = models.ManyToManyField("CustomerGroup", verbose_name=_('Is member of'), blank=True)
    isLead = models.BooleanField(default=True)

    def createContract(self, request):
        contract = koalixcrm.crm.documents.contract.Contract()
        contract.default_customer = self
        contract.default_currency = djangoUserExtension.models.UserExtension.objects.filter(user=request.user.id)[
            0].defaultCurrency
        contract.last_modified_by = request.user
        contract.staff = request.user
        contract.save()
        return contract

    def createInvoice(self, request):
        contract = self.createContract(request)
        invoice = contract.createInvoice()
        return invoice

    def createQuote(self):
        contract = self.createContract()
        quote = contract.createQuote()
        return quote

    def isInGroup(self, customerGroup):
        for customerGroupMembership in self.ismemberof.all():
            if (customerGroupMembership.id == customerGroup.id):
                return 1
        return 0

    '''def hasPerson(self, person):
        for customerContact in self.people.all():
            if (customerContact.id == person.id):
                return 1
        return 0'''

    class Meta:
        app_label = "crm"
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')

    def __str__(self):
        return '{} ({})'.format(str(self.name), self.id)

class ProductForCustomer(models.Model):
    customer = models.ForeignKey(Customer, related_name='supplier_association', blank=True, null=True)
    product = models.ForeignKey(Product, verbose_name=_("Related Product"), blank=True, null=True)
    supplier = models.ForeignKey(Supplier, related_name='customer_association', blank=True, null=True)
    service_type = models.CharField(verbose_name=_("Service Type"), max_length=100, blank=True, null=True)
    quantity = models.IntegerField(verbose_name=_("Quantity"), blank=True, null=True)
    maintainer = models.CharField(verbose_name=_("Maintainer"), max_length=100, blank=True, null=True)
    year = models.CharField(verbose_name=_("Year of installation"), max_length=50, blank=True, null=True)
    expire_date = models.DateTimeField(verbose_name=_("Expire Date"), blank=True, null=True)
    
    class Meta:
        app_label = "crm"
        verbose_name = _('Product')
        verbose_name_plural = _('Products')  

    def __str__(self):
        return str(self.id)

class SwitchboardForCustomer(ProductForCustomer):
    internal_lines = models.IntegerField(verbose_name=_("Internal lines"), blank=True, null=True)
    external_lines = models.IntegerField(verbose_name=_("External lines"), blank=True, null=True)
    
    class Meta:
        app_label = "crm"
        verbose_name = _('Switchboard')
        verbose_name_plural = _('Switchboards')  

    def __str__(self):
        return str(self.id)

class AnalogPhoneForCustomer(ProductForCustomer):
    class Meta:
        app_label = "crm"
        verbose_name = _('Analog Phone')
        verbose_name_plural = _('Analog Phones')  

    def __str__(self):
        return str(self.id)

class DigitalPhoneForCustomer(ProductForCustomer):
    class Meta:
        app_label = "crm"
        verbose_name = _('Digital Phone')
        verbose_name_plural = _('Digital Phones')  

    def __str__(self):
        return str(self.id)

class InternetForCustomer(ProductForCustomer):
    class Meta:
        app_label = "crm"
        verbose_name = _('Internet Connection')
        verbose_name_plural = _('Internet Connections')  

    def __str__(self):
        return str(self.id)

class MobileForCustomer(ProductForCustomer):
    class Meta:
        app_label = "crm"
        verbose_name = _('Mobile Service')
        verbose_name_plural = _('Mobile Services')  

    def __str__(self):
        return str(self.id)


class CustomerPhoneSystem(admin.StackedInline):
    model = SwitchboardForCustomer
    extra = 0
    classes = ['collapse']
    raw_id_fields = ("product",)
    autocomplete_lookup_fields = {
        'fk': ['product'],
    }
    fieldsets = (
        (None, {'fields': ['product']}),
        ('Additional data', {
            'fields': (
            'service_type', 'supplier', 'expire_date', 'year', 'external_lines', 'internal_lines',)
        }),
    )

    def __str__(self):
        return '{} ({})'.format(str(self.product.name), self.product.id)

class CustomerAnalogPhones(admin.StackedInline):
    model = AnalogPhoneForCustomer
    extra = 0
    classes = ['collapse']
    raw_id_fields = ("product",)
    autocomplete_lookup_fields = {
        'fk': ['product'],
    }
    fieldsets = (
        (None, {'fields': ['product']}),
        ('Additional data', {
            'fields': (
            'service_type', 'supplier', 'expire_date', 'year',)
        }),
    )

    def __str__(self):
        return '{} ({})'.format(str(self.product.name), self.product.id)

class CustomerDigitalPhones(admin.StackedInline):
    model = DigitalPhoneForCustomer
    extra = 0
    classes = ['collapse']
    raw_id_fields = ("product",)
    autocomplete_lookup_fields = {
        'fk': ['product'],
    }
    fieldsets = (
        (None, {'fields': ['product']}),
        ('Additional data', {
            'fields': (
            'service_type', 'supplier', 'expire_date', 'year',)
        }),
    )

    def __str__(self):
        return '{} ({})'.format(str(self.product.name), self.product.id)

class CustomerMobilePhones(admin.StackedInline):
    model = MobileForCustomer
    extra = 0
    classes = ['collapse']
    raw_id_fields = ("product",)
    autocomplete_lookup_fields = {
        'fk': ['product'],
    }
    fieldsets = (
        (None, {'fields': ['product']}),
        ('Additional data', {
            'fields': (
            'service_type', 'supplier', 'expire_date', 'year',)
        }),
    )

    def __str__(self):
        return '{} ({})'.format(str(self.product.name), self.product.id)

class CustomerInternetConnection(admin.StackedInline):
    model = InternetForCustomer
    extra = 0
    classes = ['collapse']
    raw_id_fields = ("product",)
    autocomplete_lookup_fields = {
        'fk': ['product'],
    }
    fieldsets = (
        (None, {'fields': ['product']}),
        ('Additional data', {
            'fields': (
            'service_type', 'supplier', 'expire_date', 'year',)
        }),
    )

    def __str__(self):
        return '{} ({})'.format(str(self.product.name), self.product.id)

'''class PhoneProviderFilter(admin.SimpleListFilter):
    title = _('Phone provider')
    parameter_name = 'phone_provider'

    def lookups(self, request, model_admin):
        list = []
        for s in Supplier.objects.all():
            list.append((s.id, _(s.name)))
        return (
            list
        )

    def queryset(self, request, queryset):
        for p in PhoneSystemForCustomer.objects.all(): 
            if self.value() == str(p.supplier.id):
                cust_per_supplier = PhoneSystemForCustomer.objects.filter(supplier=p.supplier)
                ids = [(c.customer.id) for c in cust_per_supplier]
                return queryset.filter(pk__in=ids)
        return queryset'''

class OptionCustomer(admin.ModelAdmin):
    list_display = ('id', 'name', 'defaultCustomerBillingCycle', 'get_state', 'get_town', 'dateofcreation',)
    list_filter = ('ismemberof', StateFilter, CityFilter)
    #list_display_links = ('name',)
    fieldsets = (('', {'fields': ('name', 'defaultCustomerBillingCycle', 'ismemberof',)}),)
    allow_add = True
    ordering = ('id',)
    search_fields = ('id', 'name')
    inlines = [ContactPostalAddress, ContactPhoneAddress, ContactEmailAddress, PeopleInlineAdmin, CustomerPhoneSystem, CustomerAnalogPhones, CustomerDigitalPhones, CustomerMobilePhones, CustomerInternetConnection, ContactCall, ContactVisit]
    
    pluginProcessor = PluginProcessor()
    inlines.extend(pluginProcessor.getPluginAdditions("customerInline"))

    def get_postal_address(self, obj):
        return PostalAddressForContact.objects.filter(company=obj.id).first()
    
    def get_state(self, obj):
        address = self.get_postal_address(obj)
        return address.state if address is not None else None

    get_state.short_description = _("State")

    def get_town(self, obj):
        address = self.get_postal_address(obj)
        return address.town if address is not None else None

    get_town.short_description = _("City")
    
    def createContract(self, request, queryset):
        for obj in queryset:
            contract = obj.createContract(request)
            response = HttpResponseRedirect('/admin/crm/contract/' + str(contract.id))
            return response

    createContract.short_description = _("Create Contract")

    @staticmethod
    def createQuote(self, request, queryset):
        for obj in queryset:
            quote = obj.createQuote()
            response = HttpResponseRedirect('/admin/crm/quote/' + str(quote.id))
        return response

    createQuote.short_description = _("Create Quote")

    @staticmethod
    def createInvoice(self, request, queryset):
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

