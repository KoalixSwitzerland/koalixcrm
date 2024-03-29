# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin
from django.utils.translation import gettext as _
from koalixcrm.crm.reporting.resource_price import ResourcePrice
from decimal import *
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from koalixcrm.crm.exceptions import ReportingPeriodNotFound


class Estimation(models.Model):
    """The estimation describes the estimated amount of resources which is still required to finish a task
    the estimation is done within a reporting period that is not yet closed. The estimation is done only considering
    all effective efforts that was reported in the previous and closed reporting periods"""
    id = models.BigAutoField(primary_key=True)
    task = models.ForeignKey("Task",
                             on_delete=models.CASCADE,
                             verbose_name=_('Task'),
                             blank=False,
                             null=False)
    resource = models.ForeignKey("Resource",
                                 on_delete=models.CASCADE)
    date_from = models.DateField(verbose_name=_("Estimation From"),
                                 blank=False,
                                 null=False)
    date_until = models.DateField(verbose_name=_("Estimation Until"),
                                  blank=False,
                                  null=False)
    amount = models.DecimalField(verbose_name=_("Amount"),
                                 max_digits=5,
                                 decimal_places=2,
                                 blank=True,
                                 null=True)
    status = models.ForeignKey("EstimationStatus",
                               on_delete=models.CASCADE,
                               verbose_name=_('Status of the estimation'),
                               blank=False,
                               null=False)
    reporting_period = models.ForeignKey("ReportingPeriod",
                                         on_delete=models.CASCADE,
                                         verbose_name=_('Reporting Period based on which the estimation was done'),
                                         blank=False,
                                         null=False)

    def duration_in_days(self):
        """The function returns the calculated difference between the date_until and the date_from and returns the value
        as number of days

        Args:
        no arguments needed

        Returns:
        difference between date_until and date_from (Integer)

        Raises:
        No exceptions planned"""
        duration_time_delta = self.date_until - self.date_from
        duration = duration_time_delta.days
        return duration

    def calculated_costs(self, bucket_start=None, bucket_end=None):
        """The function returns the calculated costs in total or the calculated costs within a specific start and
        stop-frame.

        Args:
        start (datetime.date)
        stop (datetime.date)

        Returns:
        planned costs (Decimal), 0 if no price can be found

        Raises:
        No exceptions planned"""
        default_resource_price = ResourcePrice.objects.filter(resource=self.resource)
        overall_costs = 0
        estimation_lies_outside_bucket = (bucket_end <= self.date_from) or bucket_start >= self.date_until
        if bucket_start >= self.date_from:
            later_start_date = bucket_start
        else:
            later_start_date = self.date_from
        if bucket_end <= self.date_until:
            earlier_end_date = bucket_end
        else:
            earlier_end_date = self.date_until

        if estimation_lies_outside_bucket:
            selected_duration = 0
        else:
            selected_duration_time_delta = earlier_end_date - later_start_date
            selected_duration = selected_duration_time_delta.days
            # Add one day because the buckets may not overlap each other. By this fact we always loose one day
            selected_duration += 1

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


class EstimationAdminForm(BaseInlineFormSet):
    def clean(self):
        """Check that the estimation is only attached to a reporting period which is not yet closed,
        also check that the date_from is at least one day before the date_until"""
        for f in self.forms:
            if any(f.errors):
                pass
            else:
                if 'date_from' in f.cleaned_data:
                    date_from = f.cleaned_data['date_from']
                else:
                    break
                date_until = f.cleaned_data['date_until']
                reporting_period = f.cleaned_data['reporting_period']
                task = f.cleaned_data['task']
                if f.cleaned_data['id']:
                    limit_of_acceptable_estimations = 1
                else:
                    limit_of_acceptable_estimations = 0
                existing_estimations = Estimation.objects.filter(reporting_period=reporting_period, task=task)
                if len(existing_estimations) > limit_of_acceptable_estimations:
                    raise ValidationError('There may only be one estimation per reporting period per task')
                try:
                    predecessor_reporting_period = reporting_period.get_predecessor(reporting_period,
                                                                                    reporting_period.project)
                    if not predecessor_reporting_period.status.is_done:
                        raise ValidationError('Please select a reporting period which has a predecessor'
                                              ' reporting period which is already in state "done"')
                except ReportingPeriodNotFound:
                    pass
                if reporting_period.status.is_done:
                    raise ValidationError('Please select a reporting period which is not yet in state "done"')
                if date_from >= date_until:
                    raise ValidationError('The date until must be at least one day after date from')


class EstimationInlineAdminView(admin.TabularInline):
    model = Estimation
    formset = EstimationAdminForm
    fieldsets = (
        (_('Work'), {
            'fields': ('task',
                       'amount',
                       'resource',
                       'date_from',
                       'date_until',
                       'status',
                       'reporting_period')
        }),
    )
    extra = 1
