# -*- coding: utf-8 -*-

from django.db import models
from django.forms import ValidationError
from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import ugettext as _
from koalixcrm.crm.documents.pdf_export import PDFExport
from koalixcrm.global_support_functions import *
from koalixcrm.crm.exceptions import ReportingPeriodDoneDeleteNotPossible
from django.contrib import messages


class Agreement(models.Model):
    task = models.ForeignKey("Task",
                             verbose_name=_('Task'),
                             blank=False,
                             null=False)
    reporting_period = models.ForeignKey("ReportingPeriod",
                                         verbose_name="Reporting Period",
                                         blank=False,
                                         null=False)
    resource = models.ForeignKey("Resource")
    resource_manager = models.ForeignKey("ResourceManager")
    unit = models.ForeignKey("Unit")
    costs = models.ForeignKey("Cost")
    agreement_type = models.ForeignKey("AgreementType")
    agreement_status = models.ForeignKey("AgreementStatus")
    agreement_from = models.DateField(verbose_name=_("Agreement From"),
                                      blank=False,
                                      null=False)
    agreement_to = models.DateField(verbose_name=_("Agreement To"),
                                    blank=False,
                                    null=False)
    agreement_amount = models.DecimalField(verbose_name=_("Amount"),
                                           max_digits=5,
                                           decimal_places=2,
                                           blank=True,
                                           null=True)

    def calculated_costs(self):
        currency = self.task.project.default_currency
        unit = self.product.default_unit

        self.product.get_costs(self, date, unit, currency)

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
