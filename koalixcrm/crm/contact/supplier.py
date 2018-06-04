# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext as _
from koalixcrm.crm.contact.contact import Contact
from koalixcrm.crm.contact.contact import ContactPostalAddress
from koalixcrm.crm.contact.contact import ContactPhoneAddress
from koalixcrm.crm.contact.contact import ContactEmailAddress


class Supplier(Contact):
    offersShipmentToCustomers = models.BooleanField(verbose_name=_("Offers Shipment to Customer"))

    class Meta:
        app_label = "crm"
        verbose_name = _('Supplier')
        verbose_name_plural = _('Suppliers')

    def __str__(self):
        return str(self.id) + ' ' + self.name


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