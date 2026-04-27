# -*- coding: utf-8 -*-

from django.contrib import admin

from koalixcrm.contacts.models.customer_billing_cycle import CustomerBillingCycle
from koalixcrm.core.admin.workspace_scoped_admin import WorkspaceScopedModelAdmin


class OptionCustomerBillingCycle(WorkspaceScopedModelAdmin, admin.ModelAdmin):
    list_display = ('id',
                    'name',
                    'time_to_payment_date',
                    'payment_reminder_time_to_payment')
    list_filter = ('workspace',)
    fieldsets = (('', {'fields': ('name',
                                  'time_to_payment_date',
                                  'payment_reminder_time_to_payment',
                                  )}),)
    allow_add = True


admin.site.register(CustomerBillingCycle, OptionCustomerBillingCycle)
