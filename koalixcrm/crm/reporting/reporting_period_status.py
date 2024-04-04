# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import gettext as _
from django.contrib import admin
from rest_framework import serializers


class ReportingPeriodStatus(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name=_("Title"),
                             max_length=250,
                             blank=False,
                             null=False)
    description = models.TextField(verbose_name=_("Text"),
                                   blank=True,
                                   null=True)
    is_done = models.BooleanField(verbose_name=_("Status represents reporting period is closed"),)

    class Meta:
        app_label = "crm"
        verbose_name = _('Reporting Period Status')
        verbose_name_plural = _('Reporting Period Status')

    def __str__(self):
        if self.title:
            return str(self.title)
        else:
            return str(self.id)


class OptionReportingPeriodStatus(admin.ModelAdmin):
    list_display = ('id',
                    'title',
                    'description',
                    'is_done')

    fieldsets = (
        (_('Task Status'), {
            'fields': ('title',
                       'description',
                       'is_done')
        }),
    )
    save_as = True


class TaskStatusJSONSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ReportingPeriodStatus
        fields = ('id',
                  'title',
                  'description',
                  'is_done')
