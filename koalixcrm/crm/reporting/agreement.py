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
        verbose_name = _('Agreement')
        verbose_name_plural = _('Agreements')


class AgreementInlineAdminView(admin.TabularInline):
    model = Agreement
    fieldsets = (
        (_('Work'), {
            'fields': ('task',
                       'resource',
                       'agreement_amount',
                       'agreement_from',
                       'agreement_to')
        }),
    )
    extra = 1
