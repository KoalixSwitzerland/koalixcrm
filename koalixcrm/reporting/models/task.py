from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Any

from django.db import models
from django.utils.html import format_html
from django.utils.translation import gettext as _

from koalixcrm import global_support_functions
from koalixcrm.core.exceptions import ReportingPeriodNotFound
from koalixcrm.core.models.workspace_scoped import WorkspaceScopedModel
from koalixcrm.reporting.models.agreement import Agreement
from koalixcrm.reporting.models.estimation import Estimation
from koalixcrm.reporting.models.resource_price import ResourcePrice
from koalixcrm.reporting.models.work import Work


class Task(WorkspaceScopedModel):
    """The Task model"""

    id = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name=_("Title"), max_length=100, blank=True, null=True)
    project = models.ForeignKey(
        "Project", on_delete=models.CASCADE, verbose_name=_("Project"), related_name="tasks", blank=False, null=False
    )
    description = models.TextField(verbose_name=_("Description"), blank=True, null=True)
    status = models.ForeignKey("TaskStatus", on_delete=models.CASCADE, verbose_name=_("Status"), blank=True, null=True)
    last_status_change = models.DateField(verbose_name=_("Last Status Change"), blank=True, null=False)
    previous_status = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(Task, self).__init__(*args, **kwargs)
        self.previous_status = self.status

    def save(self, *args: Any, **kwargs: Any) -> None:
        if self.id is not None:
            if self.status != self.previous_status:
                self.last_status_change = global_support_functions.get_today_date()
        elif self.last_status_change is None:
            self.last_status_change = global_support_functions.get_today_date()
        super(Task, self).save(*args, **kwargs)

    def link_to_task(self) -> str:
        if self.id:
            return format_html("<a href='/admin/reporting/task/%s' >%s</a>" % (str(self.id), str(self.title)))
        else:
            return "Not present"

    link_to_task.short_description = _("Task")

    def planned_duration(self) -> Any:
        if (not self.planned_start()) or (not self.planned_end()):
            duration_in_days = "n/a"
        elif self.planned_start() > self.planned_end():
            duration_in_days = "n/a"
        else:
            duration_in_days = (self.planned_end() - self.planned_start()).days
        return duration_in_days

    planned_duration.short_description = _("Planned Duration [dys]")
    planned_duration.tags = True

    def planned_start(self) -> datetime.date | None:
        """The function return the planned start of a task as a date based on the estimations which are
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
                if planned_task_start is None:
                    planned_task_start = estimation.date_from
                elif estimation.date_from < planned_task_start:
                    planned_task_start = estimation.date_from
        return planned_task_start

    planned_start.short_description = _("Planned Start")
    planned_start.tags = True

    def planned_end(self) -> datetime.date | None:
        """The function return the planned end of a task as a date based on the estimations which are
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

    planned_end.short_description = _("Planned End")
    planned_end.tags = True

    def planned_effort(self, reporting_period: Any = None, remaining: bool = False) -> Any:
        """The function return the planned effort of resources which have been estimated for this task
        at a specific reporting period. When no reporting_period is provided, the last reporting period
        is selected

        Args:
        remaining (Boolean)

        Returns:
        planned effort (Decimal) [hrs], 0 if when no estimation are present

        Raises:
        no exceptions expected"""
        latest_estimation = self.get_latest_estimation()
        effort = 0
        if latest_estimation:
            try:
                predecessor_reporting_period = latest_estimation.reporting_period.get_predecessor(
                    latest_estimation.reporting_period, latest_estimation.reporting_period.project
                )
            except ReportingPeriodNotFound:
                effort = 0
                predecessor_reporting_period = None
            if remaining:
                effort = 0
            else:
                while predecessor_reporting_period:
                    effort += self.effective_effort(reporting_period=predecessor_reporting_period)
                    try:
                        predecessor_reporting_period = predecessor_reporting_period.get_predecessor(
                            predecessor_reporting_period, predecessor_reporting_period.project
                        )
                    except ReportingPeriodNotFound:
                        predecessor_reporting_period = None
            if latest_estimation.amount is not None:
                effort += latest_estimation.amount
        else:
            effort = 0
        return effort

    planned_effort.short_description = _("Planned Effort")
    planned_effort.tags = True

    def get_latest_estimation(self) -> Any:
        estimations = Estimation.objects.filter(task=self.id)
        latest_estimation = None
        for estimation in estimations:
            if not latest_estimation:
                latest_estimation = estimation
            else:
                if latest_estimation.reporting_period.end < estimation.reporting_period.begin:
                    latest_estimation = estimation
        return latest_estimation

    def planned_costs_in_buckets(self, reporting_period: Any = None, buckets: Any = None) -> dict:
        """The function returns the planned costs of resources which have been estimated for this task
         at a specific reporting period plus the costs of the effective effort before the provided reporting_period
         When no reporting_period is provided. The costs are split into the provided buckets.
         The passed argument reporting_period is used to specify the root of the estimation.

        Args:
        bucket (list of ReportingPeriods)
        reporting_period (ReportingPeriod)

        Returns:
        planned costs (Decimal), 0 if when no estimation or no reporting period is attached to the task

        Raises:
        No exceptions planned"""
        planned_costs = dict()

        latest_estimation = self.get_latest_estimation()
        if buckets:
            for bucket in buckets:
                planned_costs[bucket] = 0
        planned_costs["sum_costs"] = 0
        if latest_estimation:
            if buckets:
                for bucket in buckets:
                    if bucket.end < latest_estimation.reporting_period.begin:
                        planned_costs[bucket] += planned_costs["sum_costs"]
                        planned_costs[bucket] += self.effective_costs(reporting_period=bucket)
                        planned_costs["sum_costs"] = planned_costs[bucket]
                    else:
                        planned_costs[bucket] += planned_costs["sum_costs"]
                        planned_costs[bucket] += latest_estimation.calculated_costs(
                            bucket_start=bucket.begin, bucket_end=bucket.end
                        )
                        planned_costs["sum_costs"] = planned_costs[bucket]
        return planned_costs

    def planned_costs(self, reporting_period: Any = None, remaining: bool = False) -> Any:
        """The function returns the planned overall costs of resources which have been estimated for this task
         at a specific reporting period plus the costs of the effective effort before the provided reporting_period
         When no reporting_period is provided, the last reporting period is selected.

        Args:
        no arguments

        Returns:
        planned costs (Decimal), 0 if when no estimation or no reporting period is present

        Raises:
        No exceptions planned"""
        planned_costs = 0
        if reporting_period:
            planned_costs_in_buckets = self.planned_costs_in_buckets(reporting_period=reporting_period, buckets=None)
            for key in planned_costs_in_buckets.keys():
                planned_costs += planned_costs_in_buckets[key]
        else:
            planned_effort = self.planned_effort(remaining=remaining)
            latest_estimation = self.get_latest_estimation()
            if latest_estimation:
                resource_prices = ResourcePrice.objects.filter(resource=latest_estimation.resource)
                price = 0
                if len(resource_prices) != 0:
                    for resource_price in resource_prices:
                        price = resource_price.price
                        break
                planned_costs = planned_effort * price
            else:
                planned_costs = 0
        return planned_costs

    planned_costs.short_description = _("Planned Costs")
    planned_costs.tags = True

    def planned_total_costs(self) -> Any:
        return self.planned_costs(remaining=False)

    planned_total_costs.short_description = _("Planned Total Costs")
    planned_total_costs.tags = True

    def effective_start(self) -> datetime.date | None:
        """The function return the effective start of a task as a date.

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

    def task_end(self) -> bool:
        """The function returns a boolean value True when the task is on
        status done.

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

    def effective_end(self) -> datetime.date | None:
        """When the task has already ended, the
        function return the effective end of a task as a date based on the reported work

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

    def effective_duration(self) -> str:
        """The function return the effective overall duration of a task as a string in days

        Args:
        no arguments

        Returns:
        duration [dys]

        Raises:
        No exceptions planned"""
        effective_end = self.effective_end()
        effective_start = self.effective_start()
        if not effective_start:
            duration_as_string = "Task has not yet started"
        elif not effective_end:
            duration_as_string = "Task has not yet ended"
        else:
            duration_as_date = self.effective_end() - self.effective_start()
            duration_as_string = duration_as_date.days.__str__()
        return duration_as_string

    effective_duration.short_description = _("Effective Duration [dys]")
    effective_duration.tags = True

    def effective_effort_overall(self) -> Decimal:
        return self.effective_effort(reporting_period=None)

    effective_effort_overall.short_description = _("Effective Effort [hrs]")
    effective_effort_overall.tags = True

    def effective_effort(self, reporting_period: Any = None) -> Decimal:
        """Effective effort returns the effective effort on a task
        when reporting_period is None, the effective effort overall is calculated
        when reporting_period is specified, the effective effort in this period is calculated"""
        if reporting_period:
            work_objects = Work.objects.filter(task=self.id, reporting_period=reporting_period)
        else:
            work_objects = Work.objects.filter(task=self.id)
        sum_effort = 0
        for work_object in work_objects:
            sum_effort += work_object.effort_seconds()
        sum_effort_in_hours = sum_effort / 3600
        return Decimal(sum_effort_in_hours)

    def effective_costs(self, reporting_period: Any = None, confirmed: bool = True) -> Decimal:
        """Returns the effective costs on a task

        Args:
          no arguments

        Returns:
          costs [Currency] (Decimal)

        Raises:
           no exception planned
        """
        agreements = Agreement.objects.filter(task=self)
        if reporting_period:
            all_work_in_task = Work.objects.filter(task=self.id, reporting_period=reporting_period)
        elif not confirmed:
            all_work_in_task = Work.objects.filter(task=self.id, reporting_period__status__is_done=False)
        else:
            all_work_in_task = Work.objects.filter(task=self.id, reporting_period__status__is_done=True)
        sum_costs = Decimal(0)
        work_with_agreement = list()
        work_without_agreement = list()
        work_calculated = list()
        human_resource_list = dict()
        for work_object in all_work_in_task:
            if work_object.human_resource not in human_resource_list:
                human_resource_list[work_object.human_resource] = dict()
            for agreement in agreements:
                agreement_matches = agreement.match_with_work(work_object)
                if agreement_matches:
                    if work_object not in work_with_agreement:
                        work_with_agreement.append(work_object)
                    if agreement not in human_resource_list.get(work_object.human_resource):
                        human_resource_list.get(work_object.human_resource)[agreement] = list()
                    human_resource_list.get(work_object.human_resource).get(agreement).append(work_object)
            if work_object not in work_with_agreement:
                work_without_agreement.append(work_object)

        for human_resource_dict in human_resource_list:
            agreement_list = Agreement.objects.filter(task=self, resource=human_resource_dict).order_by("costs__price")
            for agreement in agreement_list:
                agreement_remaining_amount = agreement.amount
                if human_resource_list[human_resource_dict].get(agreement):
                    for work in human_resource_list[human_resource_dict].get(agreement):
                        if work in work_with_agreement:
                            worked_hours = work.worked_hours if work.worked_hours is not None else Decimal(0)
                            if (agreement_remaining_amount - worked_hours) > 0:
                                agreement_remaining_amount -= worked_hours
                                sum_costs += Decimal(work.effort_hours()) * agreement.costs.price
                                work_calculated.append(work)
        for work in all_work_in_task:
            if work not in work_calculated:
                if work not in work_without_agreement:
                    work_without_agreement.append(work)
        for work in work_without_agreement:
            default_resource_prices = ResourcePrice.objects.filter(resource=work.human_resource.id).order_by("price")
            if default_resource_prices:
                default_resource_price = default_resource_prices[0]
                sum_costs += Decimal(work.effort_hours()) * default_resource_price.price
            else:
                sum_costs = Decimal(0)
                break
        sum_costs = self.project.default_currency.round(sum_costs)
        return sum_costs

    def effective_costs_confirmed(self) -> Decimal:
        return self.effective_costs()

    effective_costs_confirmed.short_description = _("Effective costs confirmed")
    effective_costs_confirmed.tags = True

    def effective_costs_not_confirmed(self) -> Decimal:
        return self.effective_costs(confirmed=False)

    effective_costs_not_confirmed.short_description = _("Effective costs not confirmed")
    effective_costs_not_confirmed.tags = True

    def is_reporting_allowed(self) -> bool:
        """Returns True when the task is available for reporting.

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

    def get_title(self) -> str:
        if self.title:
            return self.title
        else:
            return "n/a"

    def __str__(self) -> str:
        return str(self.id) + " " + self.get_title()

    class Meta:
        app_label = "reporting"
        db_table = "crm_task"
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")
