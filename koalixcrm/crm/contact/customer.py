# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext as _
from koalixcrm.plugin import *
from koalixcrm import djangoUserExtension
from koalixcrm.crm.contact.contact import Contact
from koalixcrm.crm.contact.contact import ContactPostalAddress
from koalixcrm.crm.contact.contact import ContactPhoneAddress
from koalixcrm.crm.contact.contact import ContactEmailAddress

import koalixcrm.crm.documents.contract


class Customer(Contact):
    default_customer_billing_cycle = models.ForeignKey('CustomerBillingCycle', verbose_name=_('Default Billing Cycle'))
    is_member_of = models.ManyToManyField("CustomerGroup", verbose_name=_('Is member of'), blank=True)

    def create_contract(self, request):
        contract = koalixcrm.crm.documents.contract.Contract()
        contract.default_customer = self
        contract.default_currency = djangoUserExtension.models.UserExtension.objects.filter(user=request.user.id)[
            0].defaultCurrency
        contract.last_modified_by = request.user
        contract.staff = request.user
        contract.save()
        return contract

    def create_invoice(self):
        contract = self.create_contract()
        invoice = contract.create_invoice()
        return invoice

    def create_quote(self):
        contract = self.create_contract()
        quote = contract.create_quote()
        return quote

    def is_in_group(self, customer_group):
        for customer_group_membership in self.is_member_of.all():
            if customer_group_membership.id == customer_group.id:
                return 1
        return 0

    class Meta:
        app_label = "crm"
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')

    def __str__(self):
        return str(self.id) + ' ' + self.name


class OptionCustomer(admin.ModelAdmin):
    list_display = ('id', 'name', 'default_customer_billing_cycle',)
    fieldsets = (('', {'fields': ('name', 'default_customer_billing_cycle', 'is_member_of',)}),)
    allow_add = True
    ordering = ('id',)
    search_fields = ('id', 'name')
    inlines = [ContactPostalAddress, ContactPhoneAddress, ContactEmailAddress]
    pluginProcessor = PluginProcessor()
    inlines.extend(pluginProcessor.getPluginAdditions("customerInline"))

    def create_contract(self, request, queryset):
        for obj in queryset:
            contract = obj.create_contract(request)
            response = HttpResponseRedirect('/admin/crm/contract/' + str(contract.id))
            return response

    create_contract.short_description = _("Create Contract")

    @staticmethod
    def create_quote(self, request, queryset):
        for obj in queryset:
            quote = obj.create_quote()
            response = HttpResponseRedirect('/admin/crm/quote/' + str(quote.id))
        return response

    create_quote.short_description = _("Create Quote")

    @staticmethod
    def create_invoice(self, request, queryset):
        for obj in queryset:
            invoice = obj.create_invoice()
            response = HttpResponseRedirect('/admin/crm/invoice/' + str(invoice.id))
        return response

    create_invoice.short_description = _("Create Invoice")

    def save_model(self, request, obj, form, change):
        if change:
            obj.last_modified_by = request.user
        else:
            obj.last_modified_by = request.user
            obj.staff = request.user
        obj.save()

    actions = ['create_contract', 'create_invoice', 'create_quote']
    pluginProcessor = PluginProcessor()
    inlines.extend(pluginProcessor.getPluginAdditions("customerActions"))