# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib import admin
from koalixcrm.crm.reporting.employeeassignmenttotask import EmployeeAssignmentToTask, InlineEmployeeAssignmentToTask
from koalixcrm.crm.reporting.generictasklink import InlineGenericTaskLink
from koalixcrm.crm.reporting.work import InlineWork
from datetime import *
from rest_framework import serializers
import koalixcrm


class Task(models.Model):
    short_description = models.CharField(verbose_name=_("Description"), max_length=100, blank=True, null=True)
    planned_start_date = models.DateField(verbose_name=_("Planned Start Date"), blank=False, null=False)
    planned_end_date = models.DateField(verbose_name=_("Planned End Date"), blank=False, null=False)
    project = models.ForeignKey("Contract", verbose_name=_('Contract'), blank=False, null=False)
    description = models.TextField(verbose_name=_("Description"), blank=True, null=True)
    status = models.ForeignKey("TaskStatus", verbose_name=_('Task Status'), blank=False, null=False)
    last_status_change = models.DateField(verbose_name=_("Last Status Change"), blank=True, null=False)

    def planned_duration(self):
        if (not self.planned_start_date) or (not self.planned_end_date):
            return 0
        elif self.planned_start_date > self.planned_end_date:
            return 0
        else:
            return self.last_status_change-self.start_date

    def planned_effort(self):
        assignments_to_this_task = EmployeeAssignmentToTask.objects.filter(task=self.id)
        sum_effort = 0
        for assignment_to_this_task in assignments_to_this_task:
            sum_effort += assignment_to_this_task.planned_effort
        return str(sum_effort)+" h"

    def effective_duration(self):
        if self.status.is_done:
            if self.planned_start_date > self.last_status_change:
                return 0
            else:
                return self.last_status_change - self.planned_start_date

    def effective_effort(self):
        return str(koalixcrm.crm.reporting.work.Work.get_sum_effort_in_hours(self))+" h"

    def __str__(self):
        return _("Task") + ": " + str(self.id) + " " + _("from Project") + ": " + str(self.project.id)

    class Meta:
        app_label = "crm"
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')


class OptionTask(admin.ModelAdmin):
    list_display = ('id',
                    'short_description',
                    'planned_end_date',
                    'planned_start_date',
                    'project',
                    'status',
                    'last_status_change',
                    'planned_duration',
                    'planned_effort',
                    'effective_duration',
                    'effective_effort')
    list_display_links = ('id',)
    list_filter = ('project',)
    ordering = ('-id',)

    fieldsets = (
        (_('Work'), {
            'fields': ('short_description',
                       'planned_end_date',
                       'planned_start_date',
                       'project',
                       'description',
                       'status')
        }),
    )
    save_as = True
    inlines = [InlineEmployeeAssignmentToTask,
               InlineGenericTaskLink,
               InlineWork]

    def save_model(self, request, obj, form, change):
        obj.last_status_change = date.today().__str__()
        obj.save()


class TaskJSONSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task
        fields = ('id',
                  'short_description',
                  'planned_end_date',
                  'planned_start_date',
                  'project',
                  'description',
                  'status')
