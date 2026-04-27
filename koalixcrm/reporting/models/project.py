# -*- coding: utf-8 -*-

from decimal import Decimal

from django.db import models
from django.utils.html import format_html
from django.utils.translation import gettext as _

from koalixcrm.reporting.models.reporting_period import ReportingPeriod
from koalixcrm.reporting.models.task import Task


class Project(models.Model):
    id = models.BigAutoField(primary_key=True)
    project_manager = models.ForeignKey('auth.User', on_delete=models.CASCADE, limit_choices_to={'is_staff': True},
                                        verbose_name=_("Staff"),
                                        related_name="db_rel_project_staff",
                                        blank=True,
                                        null=True)
    project_name = models.CharField(verbose_name=_("Project name"),
                                    max_length=100,
                                    null=True,
                                    blank=True)
    description = models.TextField(verbose_name=_("Description"),
                                   null=True,
                                   blank=True)
    project_status = models.ForeignKey("ProjectStatus",
                                       on_delete=models.CASCADE,
                                       verbose_name=_('Project Status'),
                                       blank=True,
                                       null=True)
    default_template_set = models.ForeignKey("djangoUserExtension.TemplateSet",
                                             on_delete=models.CASCADE,
                                             verbose_name=_("Default Template Set"),
                                             null=True,
                                             blank=True)
    default_currency = models.ForeignKey("core.Currency",
                                         on_delete=models.CASCADE,
                                         verbose_name=_("Default Currency"),
                                         null=False,
                                         blank=False)
    date_of_creation = models.DateTimeField(verbose_name=_("Created at"),
                                            auto_now_add=True)
    last_modification = models.DateTimeField(verbose_name=_("Last modified"),
                                             auto_now=True)
    last_modified_by = models.ForeignKey('auth.User',
                                         on_delete=models.CASCADE,
                                         limit_choices_to={'is_staff': True},
                                         verbose_name=_("Last modified by"),
                                         related_name="db_project_last_modified")

    def link_to_project(self):
        if self.id:
            return format_html("<a href='/admin/reporting/project/%s' >%s</a>" % (str(self.id), str(self.project_name)))
        else:
            return "Not present"
    link_to_project.short_description = _("Project")

    def get_reporting_period(self, search_date):
        """Returns the reporting period that is valid. Valid is a reporting period when the provided date
          lies between begin and end of the reporting period

        Args:
          no arguments

        Returns:
          accounting_period (ReportPeriod)

        Raises:
          ReportPeriodNotFound when there is no valid reporting Period"""
        return ReportingPeriod.get_reporting_period(self, search_date)

    def effective_costs(self, reporting_period=None, confirmed=False):
        effective_cost = 0
        for task in Task.objects.filter(project=self.id):
            effective_cost += task.effective_costs(reporting_period=reporting_period, confirmed=confirmed)
        self.default_currency.round(effective_cost)
        return effective_cost

    def effective_costs_confirmed(self):
        return self.effective_costs(confirmed=True)
    effective_costs_confirmed.short_description = _("Effective Confirmed Costs")
    effective_costs_confirmed.tags = True

    def effective_costs_not_confirmed(self):
        return self.effective_costs(confirmed=False)
    effective_costs_not_confirmed.short_description = _("Effective Not Confirmed Costs")
    effective_costs_not_confirmed.tags = True

    def effective_effort(self, reporting_period=None):
        effective_effort = 0
        for task in Task.objects.filter(project=self.id):
            effective_effort += task.effective_effort(reporting_period=reporting_period)
        return effective_effort
    effective_effort.short_description = _("Effective Accumulated effort")
    effective_effort.tags = True

    def planned_costs_in_buckets(self, reporting_period=None, buckets=None):
        """The function return the planned overall costs

        Args:
        no arguments

        Returns:
        planned costs (String)

        Raises:
        No exceptions planned"""
        planned_effort_accumulated = dict()
        planned_effort_accumulated['sum_costs'] = 0
        if buckets:
            for bucket in buckets:
                planned_effort_accumulated[bucket] = 0
        all_project_tasks = Task.objects.filter(project=self.id)
        if all_project_tasks:
            for task in all_project_tasks:
                planned_effort_accumulated_per_task = task.planned_costs_in_buckets(reporting_period, buckets)
                if buckets:
                    for bucket in buckets:
                        planned_effort_accumulated[bucket] += planned_effort_accumulated_per_task[bucket]
                planned_effort_accumulated['sum_costs'] += planned_effort_accumulated_per_task['sum_costs']

        if buckets:
            for bucket in buckets:
                planned_effort_accumulated[bucket] = Decimal(planned_effort_accumulated[bucket])
                self.default_currency.round(planned_effort_accumulated[bucket])
        planned_effort_accumulated['sum_costs'] = Decimal(planned_effort_accumulated['sum_costs'])
        self.default_currency.round(planned_effort_accumulated['sum_costs'])
        return planned_effort_accumulated

    def planned_costs(self, reporting_period=None, remaining=True):
        all_project_tasks = Task.objects.filter(project=self.id)
        planned_costs = 0
        if all_project_tasks:
            for task in all_project_tasks:
                planned_costs += task.planned_costs(reporting_period=reporting_period, remaining=remaining)
        return planned_costs

    def planned_total_costs(self):
        return self.planned_costs(remaining=False)
    planned_total_costs.short_description = _("Planned Total Costs")
    planned_total_costs.tags = True

    def effective_start(self):
        """The function return the effective start of a project as a date

        Args:
        no arguments

        Returns:
        effective_start (Date) or None when not yet started

        Raises:
        No exceptions planned"""
        no_tasks_started = True
        all_project_tasks = Task.objects.filter(project=self.id)
        effective_project_start = None
        if len(all_project_tasks) == 0:
            effective_project_start = None
        else:
            for task in all_project_tasks:
                if not effective_project_start:
                    if task.effective_start():
                        effective_project_start = task.effective_start()
                        no_tasks_started = False
                effective_task_start = task.effective_start()
                if effective_task_start:
                    if effective_task_start < effective_project_start:
                        effective_project_start = effective_task_start
            if no_tasks_started:
                effective_project_start = None
        return effective_project_start
    effective_start.short_description = _("Effective Start")
    effective_start.tags = True

    def effective_end(self):
        """The function return the effective end of a project as a date

        Args:
        no arguments

        Returns:
        effective_end (Date) or None when not yet ended

        Raises:
        No exceptions planned"""
        all_tasks_done = True
        all_project_tasks = Task.objects.filter(project=self.id)
        effective_project_end = None
        if len(all_project_tasks) == 0:
            effective_project_end = None
        else:
            i = 0
            for task in all_project_tasks:
                if not effective_project_end:
                    if not task.effective_start():
                        all_tasks_done = False
                        break
                    else:
                        effective_project_end = task.effective_start()
                effective_task_end = task.effective_end()
                if not effective_task_end:
                    all_tasks_done = False
                    break
                elif effective_task_end > effective_project_end:
                    effective_project_end = effective_task_end
                i = i+1
            if not all_tasks_done:
                effective_project_end = None
        return effective_project_end
    effective_end.short_description = _("Effective End")
    effective_end.tags = True

    def effective_duration(self):
        """The function return the effective overall duration of a project as a string in days

        Args:
        no arguments

        Returns:
        duration_in_days or description (String)

        Raises:
        No exceptions planned"""
        effective_end = self.effective_end()
        effective_start = self.effective_start()
        if not effective_start:
            duration_as_string = "Project has not yet started"
        elif not effective_end:
            duration_as_string = "Project has not yet ended"
        else:
            duration_as_date = self.effective_end()-self.effective_start()
            duration_as_string = duration_as_date.days.__str__()
        return duration_as_string
    effective_duration.short_description = _("Effective Duration [dys]")
    effective_duration.tags = True

    def planned_start(self):
        """ The function return planned overall start of a project as a date

        Args:
        no arguments

        Returns:
        planned_end (datetime.Date) or  None

        Raises:
        No exceptions planned"""
        tasks = Task.objects.filter(project=self.id)
        if tasks:
            i = 0
            project_start = None
            for task in tasks:
                if task.planned_start():
                    if i == 0:
                        project_start = task.planned_start()
                    elif task.planned_start() < project_start:
                        project_start = task.planned_start()
                    i += 1
            return project_start
        else:
            return None

    def planned_end(self):
        """The function return planned overall end of a project as a date

        Args:
        no arguments

        Returns:
        planned_end (datetime.Date)

        Raises:
        No exceptions planned"""
        tasks = Task.objects.filter(project=self.id)
        if tasks:
            i = 0
            project_end = None
            for task in tasks:
                if task.planned_end():
                    if i == 0:
                        project_end = task.planned_end()
                    elif task.planned_end() > project_end:
                        project_end = task.planned_end()
                    i += 1
                    return project_end
        else:
            return None

    def planned_duration(self):
        """The function return planned overall duration of a project as a string in days

        Args:
        no arguments

        Returns:
        duration_in_days (String)

        Raises:
        No exceptions planned"""
        if (not self.planned_start()) or (not self.planned_end()):
            duration_in_days = "n/a"
        elif self.planned_start() > self.planned_end():
            duration_in_days = "n/a"
        else:
            duration_in_days = (self.planned_end()-self.planned_start()).days.__str__()
        return duration_in_days
    planned_duration.short_description = _("Planned Duration [dys]")
    planned_duration.tags = True

    def get_project_name(self):
        if self.project_name:
            return self.project_name
        else:
            return "n/a"

    def is_reporting_allowed(self):
        """The function returns a boolean True when it is allowed to report on the project

        Args:
          no arguments

        Returns:
          reporting_allowed (Boolean)

        Raises:
          No exceptions planned"""
        reporting_periods = ReportingPeriod.objects.filter(project=self.id, status__is_done=False)
        if len(reporting_periods) != 0:
            if not self.project_status.is_done:
                return True
            else:
                return False
        else:
            return False

    def __str__(self):
        return str(self.id)+" "+self.get_project_name()

    class Meta:
        app_label = "reporting"
        db_table = "crm_project"
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')
