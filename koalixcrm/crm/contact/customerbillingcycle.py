# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _


class CustomerBillingCycle(models.Model):
    name = models.CharField(max_length=300, verbose_name=_("Name"))
    timeToPaymentDate = models.IntegerField(verbose_name=_("Days To Payment Date"))

    class Meta:
        app_label = "crm"
        verbose_name = _('Customer Billing Cycle')
        verbose_name_plural = _('Customer Billing Cycle')

    def __str__(self):
        return str(self.id) + ' ' + self.name
