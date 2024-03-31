# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin
from django.utils.translation import gettext as _
from koalixcrm.crm.reporting.resource_price import ResourcePrice


class Agreement(models.Model):
    """The Agreement describes the contract between the steer-co or the customer with the project manager"""
    id = models.BigAutoField(primary_key=True)
    task = models.ForeignKey("Task",
                             on_delete=models.CASCADE,
                             verbose_name=_('Task'),
                             blank=False,
                             null=False)
    resource = models.ForeignKey("Resource", on_delete=models.CASCADE)
    unit = models.ForeignKey("Unit", on_delete=models.CASCADE)
    costs = models.ForeignKey(ResourcePrice, on_delete=models.CASCADE)
    type = models.ForeignKey("AgreementType", on_delete=models.CASCADE)
    status = models.ForeignKey("AgreementStatus", on_delete=models.CASCADE)
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
        return 0

    def match_with_work(self, work):
        """This method checks whether the provided work can be covered by the agreement.
        the method checks whether the reported work corresponds with the resource and whether the
        reported work was within the time-frame of the agreement.
        The method returns False when the Agreement is not yet in status agreed

        Args:
          work (koalixcrm.crm.reporting.work.Work)

        Returns:
          True when no ValidationError was raised

        Raises:
          should not raise exceptions"""
        matches = False
        if self.status.is_agreed:
            if (work.date >= self.date_from) and (work.date <= self.date_until):
                if self.resource.id == work.human_resource.id:
                    matches = True
        return matches

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
                       'unit',
                       'costs',
                       'date_from',
                       'date_until',
                       'type',
                       'status')
        }),
    )
    extra = 1
