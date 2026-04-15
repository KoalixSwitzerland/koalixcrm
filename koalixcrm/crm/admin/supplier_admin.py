# -*- coding: utf-8 -*-

from django.contrib import admin
from koalixcrm.crm.contact.supplier import Supplier
from koalixcrm.crm.admin.contact_inlines import (
    ContactPostalAddress,
    ContactPhoneAddress,
    ContactEmailAddress,
)


class OptionSupplier(admin.ModelAdmin):
    list_display = ('id',
                    'name',
                    'offers_shipment_to_customers')
    fieldsets = (('',
                  {'fields': ('name',
                              'offers_shipment_to_customers')}),)
    inlines = [ContactPostalAddress, ContactPhoneAddress, ContactEmailAddress]
    allow_add = True

    def save_model(self, request, obj, form, change):
        if change:
            obj.last_modified_by = request.user
        else:
            obj.last_modified_by = request.user
            obj.staff = request.user
        obj.save()


admin.site.register(Supplier, OptionSupplier)
