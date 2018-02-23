# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext as _
from koalixcrm.plugin import *
from koalixcrm import djangoUserExtension
from koalixcrm.crm.contact.contact import Contact, ContactCall, PeopleInlineAdmin
from koalixcrm.crm.contact.supplier import Supplier
from koalixcrm.crm.product.phonesystem import PhoneSystem
from koalixcrm.crm.contact.person import *

import koalixcrm.crm.documents.contract

class Customer(Contact):
    defaultCustomerBillingCycle = models.ForeignKey('CustomerBillingCycle', verbose_name=_('Default Billing Cycle'))
    ismemberof = models.ManyToManyField("CustomerGroup", verbose_name=_('Is member of'), blank=True)

    def createContract(self, request):
        contract = koalixcrm.crm.documents.contract.Contract()
        contract.default_customer = self
        contract.default_currency = djangoUserExtension.models.UserExtension.objects.filter(user=request.user.id)[
            0].defaultCurrency
        contract.last_modified_by = request.user
        contract.staff = request.user
        contract.save()
        return contract

    def createInvoice(self):
        contract = self.createContract()
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
        return str(self.id) + ' ' + self.name

class PhoneSystemForCustomer(PhoneSystem):
    customer = models.ForeignKey(Customer, related_name='supplier_association', blank=True, null=True)
    supplier = models.ForeignKey(Supplier, related_name='customer_association', blank=True, null=True)
    service_type = models.CharField(verbose_name=_("Service Type"), max_length=100, blank=True, null=True)
    expire_date = models.DateTimeField(verbose_name=_("Expire Date"), blank=True, null=True)

    class Meta:
        app_label = "crm"
        verbose_name = _('Phone System')
        verbose_name_plural = _('Phone System')

    def __str__(self):
        return str(self.id)

class CustomerPhoneSystem(admin.StackedInline):
    model = PhoneSystemForCustomer
    extra = 1
    classes = ['collapse']
    fieldsets = (
        ('Basics', {
            'fields': (
            'system_model', 'year', 'n_phones_ana', 'n_phones_dig', 'n_ext_lines', 'service_type', 'supplier', 'expire_date',)
        }),
    )

class PhoneProviderFilter(admin.SimpleListFilter):
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
        return queryset

class OptionCustomer(admin.ModelAdmin):
    list_display = ('id', 'name', 'state', 'defaultCustomerBillingCycle',)
    list_filter = ('state', 'ismemberof', PhoneProviderFilter)
    #filter_horizontal = ('people',)
    fieldsets = (('', {'fields': ('name', 'defaultCustomerBillingCycle', 'ismemberof', 'addressline1', 
        'addressline2', 'zipcode', 'town', 'state', 'country',)}),)
    allow_add = True
    ordering = ('id',)
    search_fields = ('id', 'name')
    inlines = [PeopleInlineAdmin, ContactCall, CustomerPhoneSystem]
    
    pluginProcessor = PluginProcessor()
    inlines.extend(pluginProcessor.getPluginAdditions("customerInline"))

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

