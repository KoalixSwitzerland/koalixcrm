# -*- coding: utf-8 -*-
from __future__ import annotations

from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.core.models.workspace_scoped import WorkspaceScopedModel


class CustomerBillingCycle(WorkspaceScopedModel):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=300,
                            verbose_name=_("Name"))
    time_to_payment_date = models.IntegerField(verbose_name=_("Days To Payment Date"))
    payment_reminder_time_to_payment = models.IntegerField(verbose_name=_("Payment Reminder, Days To Payment Date "))

    class Meta:
        app_label = "contacts"
        db_table = "crm_customerbillingcycle"
        verbose_name = _('Customer Billing Cycle')
        verbose_name_plural = _('Customer Billing Cycle')

    def __str__(self) -> str:
        return self.id.__str__() + ' ' + self.name


