# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib import admin
from django.utils.html import format_html
from koalixcrm.crm.reporting.agreement import Agreement
from koalixcrm.crm.reporting.agreement import AgreementInlineAdminView
from koalixcrm.crm.reporting.estimation import EstimationInlineAdminView
from koalixcrm.crm.reporting.generic_task_link import InlineGenericTaskLink
from koalixcrm.crm.reporting.work import WorkInlineAdminView, Work
from koalixcrm.crm.reporting.reporting_period import ReportingPeriod
from koalixcrm.crm.reporting.estimation import Estimation
from koalixcrm.crm.documents.pdf_export import PDFExport
from koalixcrm.crm.exceptions import ReportingPeriodNotFound
from rest_framework import serializers
from koalixcrm import global_support_functions


class Task(models.Model):
    title = models.CharField(verbose_name=_("Title"),
                             max_length=100,
                             blank=True,
                             null=True)
    project = models.ForeignKey("Project",
                                verbose_name=_('Project'),
                                related_name='tasks',
                                blank=False,
                                null=False)
    description = models.TextField(verbose_name=_("Description"),
                                   blank=True,
                                   null=True)
    status = models.ForeignKey("TaskStatus", verbose_name=_('Status'),
                               blank=True,
                               null=True)
    last_status_change = models.DateField(verbose_name=_("Last Status Change"),
                                          blank=True,
                                          null=False)
    previous_status = None

    def __init__(self, *args, **kwargs):
        super(Task, self).__init__(*args, **kwargs)
        self.previous_status = self.status

    def save(self, *args, **kwargs):
        if self.id is not None:
            if self.status != self.previous_status:
                self.last_status_change = global_support_functions.get_today_date()
        elif self.last_status_change is None:
            self.last_status_change = global_support_functions.get_today_date()
        super().save(*args, **kwargs)

    def link_to_task(self):
        if self.id:
            return format_html("<a href='/admin/crm/task/%s' >%s</a>" % (str(self.id), str(self.title)))
        else:
            return "Not present"
    link_to_task.short_description = _("Task");

    def planned_duration(self):
        if (not self.planned_start()) or (not self.planned_end()):
            duration_in_days = "n/a"
        elif self.planned_start() > self.planned_end():
            duration_in_days = "n/a"
        else:
            duration_in_days = (self.planned_end()-self.planned_start()).days
        return duration_in_days
    planned_duration.short_description = _("Planned Duration [dys]")
    planned_duration.tags = True

    def planned_start(self):
        """ The function return the planned start of a task as a date based on the estimations which are
         attached to the task in case there was no estimation attached to this task, the function returns None

         Args:
         no arguments

         Returns:
         planned_start (Date) or None

         Raises:
         No exceptions planned"""
        all_task_estimations = Estimation.objects.filter(task=self.id)
        planned_task_start = None
        if len(all_task_estimations) == 0:
            planned_task_start = None
        else:
            for estimation in all_task_estimations:
                if not planned_task_start:
                    planned_task_start = estimation.date_from
                elif estimation.date_from < planned_task_start:
                    planned_task_start = estimation.date_from
        return planned_task_start
        planned_start.short_description = _("Planned Start")
        planned_start.tags = True

    def planned_end(self):
        """ The function return the planned end of a task as a date based on the estimations which are
         attached to the task in case there was no estimation attached to this task, the function returns None

         Args:
         no arguments

         Returns:
         planned_end (Date) or None

         Raises:
         No exceptions planned"""
        all_task_estimations = Estimation.objects.filter(task=self.id)
        planned_task_end = None
        if len(all_task_estimations) == 0:
            planned_task_end = None
        else:
            for estimation in all_task_estimations:
                if not planned_task_end:
                    planned_task_end = estimation.date_until
                elif estimation.date_until < planned_task_end:
                    planned_task_end = estimation.date_until
        return planned_task_end
        planned_start.short_description = _("Planned End")
        planned_start.tags = True

    def planned_costs(self, reporting_period=None):
        """The function return the planned costs of resources which have been estimated for this task
        at a specific reporting period. When no reporting_period is provided, the last reporting period
        is selected

        Args:
        no arguments

        Returns:
        planned costs (Decimal), 0 if when no agreements are present

        Raises:
        No exceptions planned"""
        try:
            if not reporting_period:
                reporting_period_internal = ReportingPeriod.get_reporting_period(self.project,
                                                                                 global_support_functions.get_today_date())

            else:
                reporting_period_internal = reporting_period
            agreements_to_this_task = Agreement.objects.filter(task=self.id,
                                                               reporting_period=reporting_period_internal)
            sum_costs = 0
            for agreement_to_this_task in agreements_to_this_task:
                sum_costs += agreement_to_this_task.calculated_costs
        except ReportingPeriodNotFound as e:
            sum_costs = 0
        return sum_costs
    planned_costs.short_description = _("Planned Costs")
    planned_costs.tags = True

    def effective_start(self):
        """The function return the effective start of a task as a date. The
        function return the effective start of a task as a date based on the reported work
        in case there was no work reported to this task, the planned start is used as a
        fall-back.

        Args:
        no arguments

        Returns:
        effective_start (Date)

        Raises:
        No exceptions planned"""
        all_task_works = Work.objects.filter(task=self.id)
        effective_task_start = None
        if len(all_task_works) == 0:
            effective_task_start = self.planned_start()
        else:
            for work in all_task_works:
                if not effective_task_start:
                    effective_task_start = work.date
                elif work.date < effective_task_start:
                    effective_task_start = work.date
        return effective_task_start
    effective_start.short_description = _("Effective Start")
    effective_start.tags = True

    def task_end(self):
        """The function returns a boolean value True when the task is on
        status done. In all other case (example in no status case) the function
        returns False

        Args:
        no arguments

        Returns:
        task_ended (Boolean)

        Raises:
        No exceptions planned"""
        if not self.status:
            task_ended = False
        elif self.status.is_done:
            task_ended = self.status.is_done
        else:
            task_ended = False
        return task_ended

    def effective_end(self):
        """When the task has already ended, the
        function return the effective end of a task as a date based on the reported work
        in case there was no work reported to this task, the last status change is used as a
        fall-back. When the task did not yet end, the function returns None

        Args:
        no arguments

        Returns:
        effective_end (Date) or None when not yet ended

        Raises:
        No exceptions planned"""
        all_task_works = Work.objects.filter(task=self.id)
        effective_task_end = None
        if self.task_end():
            if len(all_task_works) == 0:
                effective_task_end = self.last_status_change
            else:
                for work in all_task_works:
                    if not effective_task_end:
                        effective_task_end = work.date
                    elif work.date > effective_task_end:
                        effective_task_end = work.date
        else:
            effective_task_end = None
        return effective_task_end
    effective_end.short_description = _("Effective End")
    effective_end.tags = True

    def effective_duration(self):
        """The function return the effective overall duration of a task as a string in days
        The function is reading the effective_starts and effective_ends of the task and
        substract them from each other.

        Args:
        no arguments

        Returns:
        duration [dys]

        Raises:
        No exceptions planned"""
        effective_end = self.effective_end()
        effective_start = self.effective_start()
        if not effective_start:
            duration_as_string = 0
        elif not effective_end:
            duration_as_string = 0
        else:
            duration_as_date = self.effective_end()-self.effective_start()
            duration_as_string = duration_as_date.days.__str__()
        return duration_as_string
    effective_duration.short_description = _("Effective Duration [dys]")
    effective_duration.tags = True

    def serialize_to_xml(self, reporting_period):
        objects = [self, ]
        main_xml = PDFExport.write_xml(objects)
        if reporting_period:
            works = Work.objects.filter(task=self.id,
                                        reporting_period=reporting_period)
        else:
            works = Work.objects.filter(task=self.id)
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
                                                       self.planned_costs())
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
    effective_effort_overall.short_description = _("Effective Effort [hrs]")
    effective_effort_overall.tags = True

    def effective_effort(self, reporting_period):
        """ Effective effort returns the effective effort on a task
        when reporting_period is None, the effective effort overall is calculated
        when reporting_period is specified, the effective effort in this period is calculated"""
        if reporting_period:
            work_objects = Work.objects.filter(task=self.id,
                                               reporting_period=reporting_period)
        else:
            work_objects = Work.objects.filter(task=self.id)
        sum_effort = 0
        for work_object in work_objects:
            sum_effort += work_object.effort_seconds()
        sum_effort_in_hours = sum_effort / 3600
        return sum_effort_in_hours

    def effective_costs(self, reporting_period=None):
        """ Effective effort returns the effective costs on a task
        when reporting_period is None, the effective effort overall is calculated
        when reporting_period is specified, the effective effort in this period is calculated"""
        agreements = Agreement.objects.filter(task=self)
        for agreement in agreements:
            agreement_dict = {'id': agreement.id,
                              'human_resource': agreement.rsource,
                              'amount': agreement.amount,
                              'price': agreement.costs}
        if reporting_period:
            work_objects = Work.objects.filter(task=self.id,
                                               reporting_period=reporting_period)
        else:
            work_objects = Work.objects.filter(task=self.id)
        sum_seconds = 0
        for work_object in work_objects:
            sum_seconds += work_object.effort_seconds()
            
        return sum_costs

    def is_reporting_allowed(self):
        """Returns True when the task is available for reporting,
        Returns False when the task is not available for reporting,
        The decision whether the task is available for reporting is purely depending
        on the task_status. When the status is done or when the status is unknown,
        the task is not longer available for reporting.

        Args:
          no arguments

        Returns:
          allowed (Boolean)

        Raises:
           when there is no valid reporting Period"""
        if self.status:
            if self.status.is_done:
                allowed = False
            else:
                allowed = True
        else:
            allowed = False
        return allowed
    is_reporting_allowed.short_description = _("Reporting")
    is_reporting_allowed.tags = True

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


class TaskAdminView(admin.ModelAdmin):
    list_display = ('link_to_task',
                    'planned_start',
                    'planned_end',
                    'project',
                    'status',
                    'last_status_change',
                    'planned_duration',
                    'planned_costs',
                    'effective_duration',
                    'effective_effort_overall')
    list_display_links = ('link_to_task',)
    list_filter = ('project',)
    ordering = ('-id',)

    fieldsets = (
        (_('Work'), {
            'fields': ('title',
                       'project',
                       'description',
                       'status')
        }),
    )
    save_as = True
    inlines = [AgreementInlineAdminView,
               EstimationInlineAdminView,
               InlineGenericTaskLink,
               WorkInlineAdminView]


class TaskInlineAdminView(admin.TabularInline):
    model = Task
    readonly_fields = ('link_to_task',
                       'last_status_change',
                       'planned_start',
                       'planned_end',
                       'planned_duration',
                       'planned_costs',
                       'effective_duration',
                       'effective_duration',
                       'effective_effort_overall')
    fieldsets = (
        (_('Task'), {
            'fields': ('link_to_task',
                       'title',
                       'planned_start',
                       'planned_end',
                       'status',
                       'last_status_change',
                       'planned_duration',
                       'planned_costs',
                       'effective_duration',
                       'effective_effort_overall')
        }),
    )
    extra = 1

    def has_add_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        return False


class TaskSerializer(serializers.ModelSerializer):
    is_reporting_allowed = serializers.SerializerMethodField()

    def get_is_reporting_allowed(self, obj):
        if obj.is_reporting_allowed():
            return "True"
        else:
            return "False"

    class Meta:
        model = Task
        fields = ('id',
                  'title',
                  'planned_end',
                  'planned_start',
                  'project',
                  'description',
                  'status',
                  'is_reporting_allowed')
