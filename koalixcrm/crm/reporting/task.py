# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib import admin
from django.utils.html import format_html
from koalixcrm.crm.reporting.employeeassignmenttotask import EmployeeAssignmentToTask, InlineEmployeeAssignmentToTask
from koalixcrm.crm.reporting.generictasklink import InlineGenericTaskLink
from koalixcrm.crm.reporting.work import InlineWork
from koalixcrm.crm.documents.pdfexport import PDFExport
from datetime import *
from rest_framework import serializers
import koalixcrm


class Task(models.Model):
    title = models.CharField(verbose_name=_("Title"), max_length=100, blank=True, null=True)
    planned_start_date = models.DateField(verbose_name=_("Planned Start Date"), blank=True, null=True)
    planned_end_date = models.DateField(verbose_name=_("Planned End Date"), blank=True, null=True)
    project = models.ForeignKey("Project", verbose_name=_('Project'), blank=False, null=False)
    description = models.TextField(verbose_name=_("Description"), blank=True, null=True)
    status = models.ForeignKey("TaskStatus", verbose_name=_('Task Status'), blank=True, null=True)
    last_status_change = models.DateField(verbose_name=_("Last Status Change"), blank=True, null=False)

    def link_to_task(self):
        if self.id:
            return format_html("<a href='/admin/crm/task/%s' >%s</a>" % (str(self.id), str(self.title)))
        else:
            return "Not present"
    link_to_task.short_description = _("Task");

    def planned_duration(self):
        if (not self.planned_start_date) or (not self.planned_end_date):
            return 0
        elif self.planned_start_date > self.planned_end_date:
            return 0
        else:
            return self.planned_end_date-self.planned_start_date

    def planned_effort(self):
        assignments_to_this_task = EmployeeAssignmentToTask.objects.filter(task=self.id)
        sum_effort = 0
        for assignment_to_this_task in assignments_to_this_task:
            sum_effort += assignment_to_this_task.planned_effort
        return sum_effort

    def effective_duration(self):
        if self.status:
            if self.status.is_done:
                if self.planned_start_date > self.last_status_change:
                    return 0
                else:
                    return self.last_status_change - self.planned_start_date
        return "n/a"

    def serialize_to_xml(self, reporting_period):
        objects = [self, ]
        main_xml = PDFExport.write_xml(objects)
        if reporting_period:
            works = koalixcrm.crm.reporting.work.Work.objects.filter(task=self.id,
                                                                     reporting_period=reporting_period)
        else:
            works = koalixcrm.crm.reporting.work.Work.objects.filter(task=self.id)
        for work in works:
            work_xml = work.serialize_to_xml()
            main_xml = PDFExport.merge_xml(main_xml, work_xml)
        main_xml = PDFExport.append_element_to_pattern(main_xml,
                                                       "object/[@model='crm.task']",
                                                       "Effective_Effort_Overall",
                                                       self.effective_effort(reporting_period=None))
        if reporting_period:
            main_xml = PDFExport.append_element_to_pattern(main_xml,
                                                           "object/[@model='crm.task']",
                                                           "Effective_Effort_InPeriod",
                                                           self.effective_effort(reporting_period=reporting_period))
        main_xml = PDFExport.append_element_to_pattern(main_xml,
                                                       "object/[@model='crm.task']",
                                                       "Planned_Effort",
                                                       self.planned_effort())
        main_xml = PDFExport.append_element_to_pattern(main_xml,
                                                       "object/[@model='crm.task']",
                                                       "Effective_Duration",
                                                       self.effective_duration())
        main_xml = PDFExport.append_element_to_pattern(main_xml,
                                                       "object/[@model='crm.task']",
                                                       "Planned_Duration",
                                                       self.planned_duration())
        return main_xml

    def effective_effort_overall(self):
        return self.effective_effort(reporting_period=None)

    def effective_effort(self, reporting_period):
        """ effective effort returns the effective effort on a task
        when reporting_period is None, the effective effort overall is calculated
        when reporting_period is specified, the effective effort in this period is calculated"""
        if reporting_period:
            work_objects = koalixcrm.crm.reporting.work.Work.objects.filter(task=self.id,
                                                                            reporting_period=reporting_period)
        else:
            work_objects = koalixcrm.crm.reporting.work.Work.objects.filter(task=self.id)
        sum_effort = 0
        for work_object in work_objects:
            if (not work_object.start_time) or (not work_object.stop_time):
                sum_effort = 0
            elif work_object.start_time > work_object.stop_time:
                sum_effort += 0
            else:
                sum_effort += work_object.effort()
        sum_effort_in_hours = sum_effort / 3600
        return sum_effort_in_hours

    def get_title(self):
        if self.title:
            return self.title
        else:
            return "n/a"

    def __str__(self):
        return str(self.id) + " " + self.get_title()

    class Meta:
        app_label = "crm"
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')


class OptionTask(admin.ModelAdmin):
    list_display = ('link_to_task',
                    'planned_start_date',
                    'planned_end_date',
                    'project',
                    'status',
                    'last_status_change',
                    'planned_duration',
                    'planned_effort',
                    'effective_duration',
                    'effective_effort_overall')
    list_display_links = ('link_to_task',)
    list_filter = ('project',)
    ordering = ('-id',)

    fieldsets = (
        (_('Work'), {
            'fields': ('title',
                       'planned_start_date',
                       'planned_end_date',
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


class InlineTasks(admin.TabularInline):
    model = Task
    readonly_fields = ('link_to_task',
                       'planned_start_date',
                       'planned_end_date',
                       'status',
                       'last_status_change',
                       'planned_duration',
                       'planned_effort',
                       'effective_duration',
                       'effective_effort_overall')
    fieldsets = (
        (_('Task'), {
            'fields': ('link_to_task',
                       'planned_start_date',
                       'planned_end_date',
                       'status',
                       'last_status_change',
                       'planned_duration',
                       'planned_effort',
                       'effective_duration',
                       'effective_effort_overall')
        }),
    )
    extra = 0

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class TaskJSONSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task
        fields = ('id',
                  'title',
                  'planned_end_date',
                  'planned_start_date',
                  'project',
                  'description',
                  'status')
