# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _
import koalixcrm


class Task(models.Model):
    planned_duration = models.TimeField(verbose_name=_("Planned Duration"))
    start_date = models.DateField(verbose_name=_("Planned Start Date"), blank=False, null=False)
    planned_end_date = models.DateField(verbose_name=_("Planned End Date"), blank=False, null=False)
    project = models.ForeignKey("Contract", verbose_name=_('Contract'), blank=False, null=False)
    description = models.TextField(verbose_name=_("Text"), blank=True, null=True)
    planned_effort = models.TimeField(verbose_name=_("Planned Effort"))
    status = models.ForeignKey("TaskStatus", verbose_name=_('Task Status'), blank=False, null=False)
    last_status_change = models.DateField(verbose_name=_("Planned End Date"), blank=False, null=False)

    def effective_duration(self):
        if self.status.is_done():
            if self.start_date > self.last_status_change:
                return 0
            else:
                return self.last_status_change-self.start_date

    def effective_effort(self):
        koalixcrm.crm.reporting.Work.get_sum_of_effort(self)

    def __str__(self):
        return _("Task") + ": " + str(self.id) + " " + _("from Project") + ": " + str(self.project.id)

    class Meta:
        app_label = "crm"
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')


