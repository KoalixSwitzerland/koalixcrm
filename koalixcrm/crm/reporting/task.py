# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib import admin, messages
from koalixcrm.crm.reporting.employeeassignmenttotask import InlineEmployeeAssignmentToTask
from koalixcrm.crm.reporting.generictasklink import InlineGenericTaskLink


class Task(models.Model):
    short_description = models.CharField(verbose_name=_("Description"), max_length=100, blank=True, null=True)
    planned_duration = models.TimeField(verbose_name=_("Planned Duration"))
    planned_start_date = models.DateField(verbose_name=_("Planned Start Date"), blank=False, null=False)
    planned_end_date = models.DateField(verbose_name=_("Planned End Date"), blank=False, null=False)
    project = models.ForeignKey("Contract", verbose_name=_('Contract'), blank=False, null=False)
    description = models.TextField(verbose_name=_("Text"), blank=True, null=True)
    status = models.ForeignKey("TaskStatus", verbose_name=_('Task Status'), blank=False, null=False)
    last_status_change = models.DateField(verbose_name=_("Planned End Date"), blank=False, null=False)

    def effective_duration(self):
        if self.status.is_done():
            if self.start_date > self.last_status_change:
                return 0
            else:
                return self.last_status_change-self.start_date

    def effective_effort(self):
        koalixcrm.crm.reporting.work.Work.get_sum_of_effort(self)

    def __str__(self):
        return _("Task") + ": " + str(self.id) + " " + _("from Project") + ": " + str(self.project.id)

    class Meta:
        app_label = "crm"
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')


class OptionTask(admin.ModelAdmin):
    list_display = ('id',
                    'short_description',
                    'planned_duration',
                    'planned_end_date',
                    'planned_start_date',
                    'project',
                    'description',
                    'status',
                    'last_status_change')
    list_display_links = ('id',)
    list_filter = ('project',)
    ordering = ('-id',)

    fieldsets = (
        (_('Work'), {
            'fields': ('short_description',
                       'planned_duration',
                       'planned_end_date',
                       'planned_start_date',
                       'project',
                       'description',
                       'status',
                       'last_status_change')
        }),
    )
    save_as = True
    inlines = [InlineEmployeeAssignmentToTask,
               InlineGenericTaskLink,]
