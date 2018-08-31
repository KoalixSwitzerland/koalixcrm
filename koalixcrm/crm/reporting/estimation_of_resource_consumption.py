# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib import admin


class EstimationOfResourceConsumption(models.Model):
    task = models.ForeignKey("Task",
                             verbose_name=_('Task'),
                             blank=False,
                             null=False)
    resource_type = models.ForeignKey("Product",
                                      verbose_name="Resource Type",
                                      blank=False,
                                      null=False)
    reporting_period = models.ForeignKey("ReportingPeriod",
                                         verbose_name="Reporting Period",
                                         blank=False,
                                         null=False)
    amount = models.DecimalField(verbose_name=_("Estimated Amount"),
                                 max_digits=10,
                                 decimal_places=2,
                                 blank=True,
                                 null=True)
    start_date = models.DateField(verbose_name=_("Estimated Start"),
                                  blank=True,
                                  null=True)
    end_date = models.DateField(verbose_name=_("Estimated End"),
                                blank=True,
                                null=True)

    def calculated_costs(self):
        res

    def __str__(self):
        return _("Estimation of Resource Consumption") + ": " + str(self.id)

    class Meta:
        app_label = "crm"
        verbose_name = _('Estimation of Resource Consumption')
        verbose_name_plural = _('Estimation of Resource Consumptions')


class InlineEstimationOfResourceConsumption(admin.TabularInline):
    model = EstimationOfResourceConsumption
    fieldsets = (
        (_('Work'), {
            'fields': ('task',
                       'resource_type',
                       'amount',
                       'start_date',
                       'end_date')
        }),
    )
    extra = 1
