# -*- coding: utf-8 -*-

from django.contrib import admin
from koalixcrm.contacts.models.customer_group import CustomerGroup


class OptionCustomerGroup(admin.ModelAdmin):
    list_display = ('id', 'name')
    fieldsets = (('', {'fields': ('name',)}),)
    allow_add = True


admin.site.register(CustomerGroup, OptionCustomerGroup)
