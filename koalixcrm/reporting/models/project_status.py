# -*- coding: utf-8 -*-
from __future__ import annotations

from django.db import models
from django.utils.translation import gettext as _
from rest_framework import serializers


class ProjectStatus(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name=_("Title"),
                             max_length=250,
                             blank=False,
                             null=False)
    description = models.TextField(verbose_name=_("Text"),
                                   blank=True,
                                   null=True)
    is_done = models.BooleanField(verbose_name=_("Status represents project is done"),)

    class Meta:
        app_label = "reporting"
        db_table = "crm_projectstatus"
        verbose_name = _('Project Status')
        verbose_name_plural = _('Project Status')

    def __str__(self) -> str:
        return str(self.id) + " " + str(self.title)


class ProjectStatusJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectStatus
        fields = ('id',
                  'title',
                  'description',)
