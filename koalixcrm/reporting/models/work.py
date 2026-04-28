# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Any

from django.db import models
from django.forms import ValidationError
from django.utils.html import format_html
from django.utils.translation import gettext as _

from koalixcrm.core.exceptions import ReportingPeriodDoneDeleteNotPossible
from koalixcrm.global_support_functions import *


class Work(models.Model):
    id = models.BigAutoField(primary_key=True)
    human_resource = models.ForeignKey("HumanResource", on_delete=models.CASCADE)
    date = models.DateField(verbose_name=_("Date"),
                            blank=False,
                            null=False)
    start_time = models.DateTimeField(verbose_name=_("Start Time"),
                                      blank=True,
                                      null=True)
    stop_time = models.DateTimeField(verbose_name=_("Stop Time"),
                                     blank=True,
                                     null=True)
    worked_hours = models.DecimalField(verbose_name=_("Worked Hours"),
                                       max_digits=5,
                                       decimal_places=2,
                                       blank=True,
                                       null=True)
    short_description = models.CharField(verbose_name=_("Short Description"),
                                         max_length=300,
                                         blank=False,
                                         null=False)
    description = models.TextField(verbose_name=_("Text"),
                                   blank=True,
                                   null=True)
    task = models.ForeignKey("Task",
                             on_delete=models.CASCADE,
                             verbose_name=_('Task'),
                             blank=False,
                             null=False)
    reporting_period = models.ForeignKey("ReportingPeriod",
                                         on_delete=models.CASCADE,
                                         verbose_name=_('Reporting Period'),
                                         blank=False,
                                         null=False)

    def link_to_work(self) -> str:
        if self.id:
            return format_html("<a href='/admin/reporting/work/%s' >%s</a>" % (str(self.id), str(self.id)))
        else:
            return "Not present"
    link_to_work.short_description = _("Work")

    def get_short_description(self) -> str:
        if self.short_description:
            return self.short_description
        elif self.description:
            return limit_string_length(self.description, 100)
        else:
            return _("Please add description")
    get_short_description.short_description = _("Short description")

    def effort_hours(self) -> float:
        if self.effort_seconds() != 0:
            return self.effort_seconds()/3600
        else:
            return 0

    def effort_seconds(self) -> float:
        if not self.start_stop_pattern_complete() and not bool(self.worked_hours):
            return 0
        elif (not bool(self.stop_time)) or (not bool(self.start_time)):
            return float(self.worked_hours)*3600
        else:
            return (self.stop_time - self.start_time).total_seconds()

    def effort_as_string(self) -> str:
        return str(self.effort_hours()) + " h"

    def start_stop_pattern_complete(self) -> bool:
        return bool(self.start_time) & bool(self.stop_time)

    def start_stop_pattern_stop_missing(self) -> bool:
        return bool(self.start_time) & (not bool(self.stop_time))

    def start_stop_pattern_start_missing(self) -> bool:
        return bool(self.stop_time) & (not bool(self.start_time))

    def __str__(self) -> str:
        return _("Work") + ": " + str(self.id) + " " + _("from Person") + ": " + str(self.human_resource.id)

    def check_working_hours(self) -> bool:
        """This method checks that the working hour is correctly provided either using the start_stop pattern
        or by providing the worked_hours in total.

        Args:

        Returns:
          True when no ValidationError was raised

        Raises:
          may raise ValidationError exception"""
        if self.start_stop_pattern_complete() & bool(self.worked_hours):
            raise ValidationError('Please either set the start, stop time or worked hours (not both)', code='invalid')
        elif self.start_stop_pattern_start_missing() or self.start_stop_pattern_stop_missing():
            raise ValidationError('Set start and stop time', code='invalid')
        return True

    def clean(self) -> Any:
        cleaned_data = super(Work, self).clean()
        self.check_working_hours()
        return cleaned_data

    def confirmed(self) -> bool:
        return self.reporting_period.status.is_done
    confirmed.short_description = _("Confirmed")
    confirmed.tags = True

    def delete(self, using: Any = None, keep_parents: bool = False) -> Any:
        if self.confirmed():
            raise ReportingPeriodDoneDeleteNotPossible("It was not possible to delete the work")
        else:
            super(Work, self).delete(using, keep_parents)

    def save(self, *args: Any, **kwargs: Any) -> None:
        if self.confirmed():
            raise ReportingPeriodDoneDeleteNotPossible("It was not possible to update the work")
        else:
            super(Work, self).save(*args, **kwargs)

    class Meta:
        app_label = "reporting"
        db_table = "crm_work"
        verbose_name = _('Work')
        verbose_name_plural = _('Work')
