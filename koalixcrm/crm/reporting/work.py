# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _


class Work(models.Model):
    employee = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True}, blank=True, verbose_name=_("Staff"),
                              related_name="db_relscstaff", null=True)
    date =models.DateField(verbose_name=_("Date"), blank=False, null=False)
    start_time = models.TimeField(verbose_name=_("Start Time"), blank=False, null=False)
    stop_time = models.TimeField(verbose_name=_("Stop Time"), blank=False, null=False)
    short_description = models.CharField(verbose_name=_("Short Description"), max_length=300, blank=False, null=False)
    description = models.TextField(verbose_name=_("Text"), blank=True, null=True)
    task = models.ForeignKey("Task", verbose_name=_('Task'), blank=False, null=False)
    work_category = models.ForeignKey("WorkCategory", verbose_name=_('Task'), blank=False, null=False)

    def __str__(self):
        return _("Work") + ": " + str(self.id) + " " + _("from Person") + ": " + str(self.employee.id)

    class Meta:
        app_label = "crm"
        verbose_name = _('Work')
        verbose_name_plural = _('Work')

class WorkCategory(models.Model):
    title = models.CharField(verbose_name=_("Title"), max_length=300, blank=False, null=False)
    description = models.TextField(verbose_name=_("Text"), blank=True, null=True)

    class Meta:
        app_label = "crm"
        verbose_name = _('Work Category')
        verbose_name_plural = _('Work Category')

class EmployeeAssignmentToTask(models.Model):
    employee = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True}, blank=True, verbose_name=_("Staff"),
                              related_name="db_relscstaff", null=True)
    effort = models.TimeField(verbose_name=_("Effort"))


class Task(models.Model):
    planned_duration = models.TimeField(verbose_name=_("Planned Duration"))
    planned_start_date =models.DateField(verbose_name=_("Planned Start Date"), blank=False, null=False)
    planned_end_date =models.DateField(verbose_name=_("Planned End Date"), blank=False, null=False)
    project = models.ForeignKey("Contract", verbose_name=_('Contract'), blank=False, null=False)


    def effective_duration(self):

    def __str__(self):
        return _("Work") + ": " + str(self.id) + " " + _("from Person") + ": " + str(self.employee.id)

    class Meta:
        app_label = "crm"
        verbose_name = _('Work')
        verbose_name_plural = _('Work')
