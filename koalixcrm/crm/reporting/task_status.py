# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import gettext as _
from django.contrib import admin
from rest_framework import serializers


class TaskStatus(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name=_("Title"), max_length=250, blank=False, null=False)
    description = models.TextField(verbose_name=_("Text"), blank=True, null=True)
    is_done = models.BooleanField(verbose_name=_("Status represents task done"),)

    class Meta:
        app_label = "crm"
        verbose_name = _('Task Status')
        verbose_name_plural = _('Task Status')

    def __str__(self):
        return str(self.id) + " " + str(self.title)


class OptionTaskStatus(admin.ModelAdmin):
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
        model = TaskStatus
        fields = ('id',
                  'title',
                  'description',)
