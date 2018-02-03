# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _


class EmployeeAssignmentToTask(models.Model):
    employee = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True}, blank=True, verbose_name=_("Staff"),
                              related_name="db_relscstaff", null=True)
    planned_effort = models.TimeField(verbose_name=_("Effort"))