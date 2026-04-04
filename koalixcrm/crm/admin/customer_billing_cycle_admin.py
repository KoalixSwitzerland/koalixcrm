# -*- coding: utf-8 -*-

from django.contrib import admin
from koalixcrm.crm.contact.customer_billing_cycle import CustomerBillingCycle


class OptionCustomerBillingCycle(admin.ModelAdmin):
    list_display = ('id',
                    'name',
                    'time_to_payment_date',
                    'payment_reminder_time_to_payment')
    fieldsets = (('', {'fields': ('name',
                                  'time_to_payment_date',
                                  'payment_reminder_time_to_payment',
                                  )}),)
    allow_add = True


admin.site.register(CustomerBillingCycle, OptionCustomerBillingCycle)
