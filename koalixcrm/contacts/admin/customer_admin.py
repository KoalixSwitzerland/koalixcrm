# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.contrib import admin
from django.utils.translation import gettext as _
from koalixcrm.plugin import PluginProcessor
from koalixcrm.contacts.models.customer import Customer
from koalixcrm.contacts.models.contact import PostalAddressForContact
from koalixcrm.contacts.admin.contact_inlines import (
    ContactPostalAddress,
    ContactPhoneAddress,
    ContactEmailAddress,
    PeopleInlineAdmin,
    ContactCall,
    ContactVisit,
    StateFilter,
    CityFilter,
)


class IsLeadFilter(admin.SimpleListFilter):
    title = _('Is lead')
    parameter_name = 'is_lead'

    def lookups(self, request, model_admin):
        return (
            ('lead', _('Lead')),
            ('customer', _('Customer')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'lead':
            return queryset.filter(is_lead=True)
        elif self.value() == 'customer':
            return queryset.filter(is_lead=False)
        else:
            return queryset


class OptionCustomer(admin.ModelAdmin):
    list_display = ('id',
                    'name',
                    'default_customer_billing_cycle',
                    'get_state',
                    'get_town',
                    'date_of_creation',
                    'get_is_lead',)
    list_filter = ('is_member_of', StateFilter, CityFilter, IsLeadFilter)
    fieldsets = (('', {'fields': ('name',
                                  'default_customer_billing_cycle',
                                  'is_member_of',)}),)
    allow_add = True
    ordering = ('id',)
    search_fields = ('id', 'name')
    inlines = [ContactPostalAddress,
               ContactPhoneAddress,
               ContactEmailAddress,
               PeopleInlineAdmin,
               ContactCall,
               ContactVisit]
    pluginProcessor = PluginProcessor()
    inlines.extend(pluginProcessor.getPluginAdditions("customerInline"))

    @staticmethod
    def get_postal_address(obj):
        return PostalAddressForContact.objects.filter(person=obj.id).first()

    def get_state(self, obj):
        address = self.get_postal_address(obj)
        return address.state if address is not None else None

    get_state.short_description = _("State")

    def get_town(self, obj):
        address = self.get_postal_address(obj)
        return address.town if address is not None else None

    get_town.short_description = _("City")

    @staticmethod
    def get_is_lead(obj):
        return obj.is_lead

    get_is_lead.short_description = _("Is Lead")

    def create_contract(self, request, queryset):
        for obj in queryset:
            contract = obj.create_contract(request)
            response = HttpResponseRedirect('/admin/contract_object_management/contract/' + str(contract.id))
            return response

    create_contract.short_description = _("Create Contract")

    @staticmethod
    def create_quotation(self, request, queryset):
        for obj in queryset:
            quotation = obj.create_quotation(request)
            response = HttpResponseRedirect('/admin/contract_object_management/quotation/' + str(quotation.id))
        return response

    create_quotation.short_description = _("Create Quotation")

    @staticmethod
    def create_invoice(self, request, queryset):
        for obj in queryset:
            invoice = obj.create_invoice(request)
            response = HttpResponseRedirect('/admin/contract_object_management/invoice/' + str(invoice.id))
        return response

    create_invoice.short_description = _("Create Invoice")

    def save_model(self, request, obj, form, change):
        if change:
            obj.last_modified_by = request.user
        else:
            obj.last_modified_by = request.user
            obj.staff = request.user
        obj.save()

    actions = ['create_contract', 'create_invoice', 'create_quotation']
    pluginProcessor = PluginProcessor()
    inlines.extend(pluginProcessor.getPluginAdditions("customerActions"))


admin.site.register(Customer, OptionCustomer)
