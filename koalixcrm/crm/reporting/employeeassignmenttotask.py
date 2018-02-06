# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _


class EmployeeAssignmentToTask(models.Model):
    employee = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True}, blank=True, verbose_name=_("Staff"),
                              related_name="db_relscstaff", null=True)
    planned_effort = models.TimeField(verbose_name=_("Effort"))
    task = models.ForeignKey("Task", verbose_name=_('Task'), blank=False, null=False)

    def __str__(self):
        return _("Employee Assignment") + ": " + str(self.employee.first_name)

    class Meta:
        app_label = "crm"
        verbose_name = _('Employee Assignment')
        verbose_name_plural = _('Employee Assignments')