# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib import admin


class EmployeeAssignmentToTask(models.Model):
    employee = models.ForeignKey("djangoUserExtension.UserExtension")
    planned_effort = models.DecimalField(verbose_name=_("Effort"), max_digits=10, decimal_places=2)
    task = models.ForeignKey("Task", verbose_name=_('Task'), blank=False, null=False)

    def __str__(self):
        return _("Employee Assignment") + ": " + str(self.employee.user.first_name)

    class Meta:
        app_label = "crm"
        verbose_name = _('Employee Assignment')
        verbose_name_plural = _('Employee Assignments')


class InlineEmployeeAssignmentToTask(admin.TabularInline):
    model = EmployeeAssignmentToTask
    fieldsets = (
        (_('Work'), {
            'fields': ('employee',
                       'planned_effort',)
        }),
    )
    extra = 1