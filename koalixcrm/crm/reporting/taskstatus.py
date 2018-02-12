# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib import admin, messages


class TaskStatus(models.Model):
    title = models.CharField(verbose_name=_("Title"), max_length=250, blank=False, null=False)
    description = models.TextField(verbose_name=_("Text"), blank=True, null=True)

    class Meta:
        app_label = "crm"
        verbose_name = _('Task Status')
        verbose_name_plural = _('Task Status')

    def __str__(self):
        return _("Task Status") + " ID: " + str(self.id) + " title: " + str(self.title)


class OptionTaskStatus(admin.ModelAdmin):
    list_display = ('id',
                    'title',
                    'description',)

    fieldsets = (
        (_('Work'), {
            'fields': ('title',
                       'description',)
        }),
    )
    save_as = True
