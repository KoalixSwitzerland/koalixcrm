# -*- coding: utf-8 -*-

from django.db import models
from django.forms import ValidationError
from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import ugettext as _
from koalixcrm.crm.documents.pdfexport import PDFExport
from koalixcrm.globalSupportFunctions import *
from koalixcrm.crm.exceptions import ReportingPeriodDoneDeleteNotPossible
from django.contrib import messages


class Work(models.Model):
    employee = models.ForeignKey("djangoUserExtension.UserExtension")
    date = models.DateField(verbose_name=_("Date"), blank=False, null=False)
    start_time = models.DateTimeField(verbose_name=_("Start Time"), blank=True, null=True)
    stop_time = models.DateTimeField(verbose_name=_("Stop Time"), blank=True, null=True)
    worked_hours = models.DecimalField(verbose_name=_("Worked Hours"),
                                       max_digits=5,
                                       decimal_places=2,
                                       blank=True,
                                       null=True)
    short_description = models.CharField(verbose_name=_("Short Description"), max_length=300, blank=False, null=False)
    description = models.TextField(verbose_name=_("Text"), blank=True, null=True)
    task = models.ForeignKey("Task", verbose_name=_('Task'), blank=False, null=False)
    reporting_period = models.ForeignKey("ReportingPeriod", verbose_name=_('Reporting Period'), blank=False, null=False)

    def link_to_work(self):
        if self.id:
            return format_html("<a href='/admin/crm/work/%s' >%s</a>" % (str(self.id), str(self.id)))
        else:
            return "Not present"
    link_to_work.short_description = _("Work")

    def get_short_description(self):
        if self.short_description:
            return self.short_description
        elif self.description:
            return limit_string_length(self.description, 100)
        else:
            return _("Please add description")
    get_short_description.short_description = _("Short description");

    def serialize_to_xml(self):
        objects = [self, ]
        main_xml = PDFExport.write_xml(objects)
        return main_xml

    def effort_hours(self):
        if self.effort_seconds() != 0:
            return self.effort_seconds()/3600
        else:
            return 0

    def effort_seconds(self):
        if not self.start_stop_pattern_complete() and not bool(self.worked_hours):
            return 0
        elif (not bool(self.stop_time)) or (not bool(self.start_time)):
            return float(self.worked_hours)*3600
        else:
            return (self.stop_time - self.start_time).total_seconds()

    def effort_as_string(self):
        return str(self.effort_hours()) + " h"

    def start_stop_pattern_complete(self):
        return bool(self.start_time) & bool(self.stop_time)

    def start_stop_pattern_stop_missing(self):
        return bool(self.start_time) & (not bool(self.stop_time))

    def start_stop_pattern_start_missing(self):
        return bool(self.stop_time) & (not bool(self.start_time))

    def __str__(self):
        return _("Work") + ": " + str(self.id) + " " + _("from Person") + ": " + str(self.employee.id)

    def check_working_hours(self):
        """This method checks that the working hour is correctly proved either using the start_stop pattern
        or by providing the worked_hours in total.

        Args:
          cleaned_data (Dict):  The cleaned_data must contain the values form the form validation.
          The django built in form validation must already have been passed

        Returns:
          True when no ValidationError was raised

        Raises:
          may raise ValidationError exception"""
        if self.start_stop_pattern_complete() & bool(self.worked_hours):
            raise ValidationError('Please either set the start, stop time or worked hours (not both)', code='invalid')
        elif self.start_stop_pattern_start_missing() or self.start_stop_pattern_stop_missing():
            raise ValidationError('Set start and stop time', code='invalid')
        return True

    def clean(self):
        cleaned_data = super(Work, self).clean()
        self.check_working_hours()
        return cleaned_data

    def delete(self):
        if self.reporting_period.status.is_done:
            raise ReportingPeriodDoneDeleteNotPossible()
        else:
            super(Work, self).delete()

    class Meta:
        app_label = "crm"
        verbose_name = _('Work')
        verbose_name_plural = _('Work')


class OptionWork(admin.ModelAdmin):
    list_display = ('link_to_work',
                    'employee',
                    'task',
                    'get_short_description',
                    'date',
                    'reporting_period',
                    'effort_as_string')

    list_filter = ('task', 'date')
    ordering = ('-id',)

    fieldsets = (
        (_('Work'), {
            'fields': ('employee',
                       'date',
                       'start_time',
                       'stop_time',
                       'worked_hours',
                       'short_description',
                       'description',
                       'task',
                       'reporting_period',)
        }),
    )
    save_as = True

    actions = ['delete_selected', ]

    def delete_selected(self, request, queryset):
        for obj in queryset:
            if obj.reporting_period.status.is_done:
                self.message_user(request, _("Delete is not allowed because the work"
                                             " is used in a reporting period which is marked "
                                             "'as done'"),
                                  level=messages.ERROR)
            else:
                obj.delete()

    delete_selected.short_description = _("Delete Selected Work")


class InlineWork(admin.TabularInline):
    model = Work
    readonly_fields = ('link_to_work',
                       'get_short_description',
                       'employee',
                       'date',
                       'effort_as_string',)
    fieldsets = (
        (_('Work'), {
            'fields': ('link_to_work',
                       'get_short_description',
                       'employee',
                       'date',
                       'effort_as_string',)
        }),
    )
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
