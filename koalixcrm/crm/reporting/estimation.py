# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext as _
from koalixcrm.crm.reporting.resource_price import ResourcePrice
from decimal import *


class Estimation(models.Model):
    task = models.ForeignKey("Task",
                             verbose_name=_('Task'),
                             blank=False,
                             null=False)
    resource = models.ForeignKey("Resource")
    date_from = models.DateField(verbose_name=_("Estimation From"),
                                 blank=False,
                                 null=False)
    date_until = models.DateField(verbose_name=_("Estimation To"),
                                  blank=False,
                                  null=False)
    amount = models.DecimalField(verbose_name=_("Amount"),
                                 max_digits=5,
                                 decimal_places=2,
                                 blank=True,
                                 null=True)
    status = models.ForeignKey("EstimationStatus",
                               verbose_name=_('Status of the estimation'),
                               blank=False,
                               null=False)
    reporting_period = models.ForeignKey("ReportingPeriod",
                                         verbose_name=_('Reporting Period based on which the estimation was done'),
                                         blank=False,
                                         null=False)

    def duration_in_days(self):
        duration_time_delta = self.date_until-self.date_from
        duration = duration_time_delta.days
        return duration

    def calculated_costs(self, start=None, end=None):
        """The function returns the calculated costs in total or the calculated costs within a specific start and
        stop-frame.

        Args:
        start (datetime.date)
        stop (datetime.date)

        Returns:
        planned costs (Decimal), 0 if no price can be found

        Raises:
        No exceptions planned"""
        default_resource_price = ResourcePrice.objects.filter(id=self.resource.id)
        if start and end:
            if start >= self.date_from and self.date_until <= end:
                selected_duration_time_delta = end-start
            elif start >= self.date_from and self.date_until > end:
                selected_duration_time_delta = self.date_until-start
            elif start < self.date_from and self.date_until <= end:
                selected_duration_time_delta = end-self.date_from
            else:
                selected_duration_time_delta = end-end
            selected_duration = selected_duration_time_delta.days
        else:
            selected_duration = self.duration_in_days()
        if len(default_resource_price) == 0:
            overall_costs = 0
        else:
            for resource_price in default_resource_price:
                overall_costs = self.amount*resource_price.price
                break
        if self.duration_in_days() <= selected_duration:
            costs = overall_costs
        else:
            costs = overall_costs * Decimal((selected_duration / self.duration_in_days()))
        return costs

    def __str__(self):
        return _("Estimation of Resource Consumption") + ": " + str(self.id)

    class Meta:
        app_label = "crm"
        verbose_name = _('Estimation of Resource Consumption')
        verbose_name_plural = _('Estimation of Resource Consumptions')


class EstimationInlineAdminView(admin.TabularInline):
    model = Estimation
    fieldsets = (
        (_('Work'), {
            'fields': ('task',
                       'resource',
                       'amount',
                       'date_from',
                       'date_until',
                       'status',
                       'reporting_period')
        }),
    )
    extra = 1
