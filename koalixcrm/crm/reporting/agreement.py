# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext as _
from koalixcrm.crm.reporting.resource_price import ResourcePrice


class Agreement(models.Model):
    task = models.ForeignKey("Task",
                             verbose_name=_('Task'),
                             blank=False,
                             null=False)
    resource = models.ForeignKey("Resource")
    unit = models.ForeignKey("Unit")
    costs = models.ForeignKey(ResourcePrice)
    type = models.ForeignKey("AgreementType")
    status = models.ForeignKey("AgreementStatus")
    date_from = models.DateField(verbose_name=_("Agreement From"),
                                 blank=False,
                                 null=False)
    date_until = models.DateField(verbose_name=_("Agreement To"),
                                  blank=False,
                                  null=False)
    amount = models.DecimalField(verbose_name=_("Amount"),
                                 max_digits=5,
                                 decimal_places=2,
                                 blank=True,
                                 null=True)

    def calculated_costs(self):
        currency = self.task.project.default_currency
        unit = self.product.default_unit

        self.product.get_costs(self, date, unit, currency)

    def __str__(self):
        return _("Agreement of Resource Consumption") + ": " + str(self.id)

    class Meta:
        app_label = "crm"
        verbose_name = _('Agreement')
        verbose_name_plural = _('Agreements')


class AgreementInlineAdminView(admin.TabularInline):
    model = Agreement
    fieldsets = (
        (_('Work'), {
            'fields': ('task',
                       'resource',
                       'amount',
                       'date_from',
                       'date_until',
                       'type',
                       'status')
        }),
    )
    extra = 1
