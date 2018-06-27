# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin
from koalixcrm.crm.documents.pdfexport import PDFExport
from django.utils.translation import ugettext as _


class Work(models.Model):
    employee = models.ForeignKey("djangoUserExtension.UserExtension")
    date = models.DateField(verbose_name=_("Date"), blank=False, null=False)
    start_time = models.DateTimeField(verbose_name=_("Start Time"), blank=False, null=False)
    stop_time = models.DateTimeField(verbose_name=_("Stop Time"), blank=False, null=False)
    short_description = models.CharField(verbose_name=_("Short Description"), max_length=300, blank=False, null=False)
    description = models.TextField(verbose_name=_("Text"), blank=True, null=True)
    task = models.ForeignKey("Task", verbose_name=_('Task'), blank=False, null=False)
    reporting_period = models.ForeignKey("ReportingPeriod", verbose_name=_('Reporting Period'), blank=False, null=False)

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
    list_display = ('id',
                    'employee',
                    'task',
                    'short_description',
                    'date',
                    'start_time',
                    'stop_time',
                    'reporting_period',
                    'effort_as_string',)

    list_display_links = ('id',)
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
    readonly_fields = ('employee',
                       'short_description',
                       'date',
                       'start_time',
                       'stop_time',
                       'effort_as_string',)
    fieldsets = (
        (_('Work'), {
            'fields': ('employee',
                       'short_description',
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
