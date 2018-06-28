# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import ugettext as _
from koalixcrm.crm.documents.pdfexport import PDFExport
from koalixcrm.globalSupportFunctions import *


class Work(models.Model):
    employee = models.ForeignKey("djangoUserExtension.UserExtension")
    date = models.DateField(verbose_name=_("Date"), blank=False, null=False)
    start_time = models.DateTimeField(verbose_name=_("Start Time"), blank=False, null=False)
    stop_time = models.DateTimeField(verbose_name=_("Stop Time"), blank=False, null=False)
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

    def effort(self):
        if not self.stop_time or not self.start_time:
            return 0
        else:
            return (self.stop_time - self.start_time).total_seconds()

    def effort_as_string(self):
        return str(self.effort()/3600) + " h"

    def __str__(self):
        return _("Work") + ": " + str(self.id) + " " + _("from Person") + ": " + str(self.employee.id)

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
                    'start_time',
                    'stop_time',
                    'reporting_period',
                    'effort_as_string',)

    list_filter = ('task', 'date')
    ordering = ('-id',)

    fieldsets = (
        (_('Work'), {
            'fields': ('employee',
                       'date',
                       'start_time',
                       'stop_time',
                       'short_description',
                       'description',
                       'task',
                       'reporting_period',)
        }),
    )
    save_as = True


class InlineWork(admin.TabularInline):
    model = Work
    readonly_fields = ('link_to_work',
                       'get_short_description',
                       'employee',
                       'date',
                       'start_time',
                       'stop_time',
                       'effort_as_string',)
    fieldsets = (
        (_('Work'), {
            'fields': ('link_to_work',
                       'get_short_description',
                       'employee',
                       'date',
                       'start_time',
                       'stop_time',
                       'effort_as_string',)
        }),
    )
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
