# -*- coding: utf-8 -*-

from django.contrib import admin
from koalixcrm.crm.contact.customer_group import CustomerGroup


class OptionCustomerGroup(admin.ModelAdmin):
    list_display = ('id', 'name')
    fieldsets = (('', {'fields': ('name',)}),)
    allow_add = True


admin.site.register(CustomerGroup, OptionCustomerGroup)
