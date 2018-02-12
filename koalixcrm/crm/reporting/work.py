# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib import admin, messages


class Work(models.Model):
    employee = models.ForeignKey("djangoUserExtension.UserExtension")
    date = models.DateField(verbose_name=_("Date"), blank=False, null=False)
    start_time = models.DateTimeField(verbose_name=_("Start Time"), blank=False, null=False)
    stop_time = models.DateTimeField(verbose_name=_("Stop Time"), blank=False, null=False)
    short_description = models.CharField(verbose_name=_("Short Description"), max_length=300, blank=False, null=False)
    description = models.TextField(verbose_name=_("Text"), blank=True, null=True)
    task = models.ForeignKey("Task", verbose_name=_('Task'), blank=False, null=False)

    @staticmethod
    def get_sum_effort(task):
        work_objects = Work.objects.filter(task=task.id)
        sum_effort = 0
        for work_object in work_objects:
            if work_object.start_time > work_object.stop_time:
                sum_effort += 0
            else:
                sum_effort += work_object.stop_time-work_object.start_time

    def __str__(self):
        return _("Work") + ": " + str(self.id) + " " + _("from Person") + ": " + str(self.employee.id)

    class Meta:
        app_label = "crm"
        verbose_name = _('Work')
        verbose_name_plural = _('Work')


class OptionWork(admin.ModelAdmin):
    list_display = ('id',
                    'employee',
                    'date',
                    'start_time',
                    'stop_time',
                    'short_description',
                    'description',
                    'task')
    list_display_links = ('id',)
    list_filter = ('task',)
    ordering = ('-id',)

    fieldsets = (
        (_('Work'), {
            'fields': ('employee',
                       'date',
                       'start_time',
                       'stop_time',
                       'short_description',
                       'description',
                       'task')
        }),
    )
    save_as = True
