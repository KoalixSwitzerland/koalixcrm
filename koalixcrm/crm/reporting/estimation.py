# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext as _
from koalixcrm.crm.product.unit import Unit


class Estimation(models.Model):
    task = models.ForeignKey("Task",
                             verbose_name=_('Task'),
                             blank=False,
                             null=False)
    resource = models.ForeignKey("Resource")
    estimation_from = models.DateField(verbose_name=_("Estimation From"),
                                       blank=False,
                                       null=False)
    estimation_to = models.DateField(verbose_name=_("Estimation To"),
                                     blank=False,
                                     null=False)
    estimation_amount = models.DecimalField(verbose_name=_("Amount"),
                                            max_digits=5,
                                            decimal_places=2,
                                            blank=True,
                                            null=True)

    def calculated_costs(self):
        currency = self.task.project.default_currency
        unit = Unit.objects.filter(short_name="hrs")
        date = self.estimation_from

        self.product.get_costs(self, unit, date, currency)

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
                       'estimation_amount',
                       'estimation_from',
                       'estimation_to')
        }),
    )
    extra = 1
