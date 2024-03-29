# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin
from django.utils.translation import gettext as _


class CustomerBillingCycle(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=300,
                            verbose_name=_("Name"))
    time_to_payment_date = models.IntegerField(verbose_name=_("Days To Payment Date"))
    payment_reminder_time_to_payment = models.IntegerField(verbose_name=_("Payment Reminder, Days To Payment Date "))

    class Meta:
        app_label = "crm"
        verbose_name = _('Customer Billing Cycle')
        verbose_name_plural = _('Customer Billing Cycle')

    def __str__(self):
        return self.id.__str__() + ' ' + self.name


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
