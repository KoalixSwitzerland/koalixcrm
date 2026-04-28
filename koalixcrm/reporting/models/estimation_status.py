# -*- coding: utf-8 -*-
from __future__ import annotations

from django.db import models
from django.utils.translation import gettext as _
from rest_framework import serializers


class EstimationStatus(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name=_("Title"),
                             max_length=250,
                             blank=False,
                             null=False)
    description = models.TextField(verbose_name=_("Text"),
                                   blank=True,
                                   null=True)
    is_obsolete = models.BooleanField(verbose_name=_("Status represents estimation is obsolete"),)

    class Meta:
        app_label = "reporting"
        db_table = "crm_estimationstatus"
        verbose_name = _('Estimation Status')
        verbose_name_plural = _('Estimation Status')

    def __str__(self) -> str:
        return str(self.id) + " " + str(self.title)


class EstimationStatusJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstimationStatus
        fields = ('id',
                  'title',
                  'description',)
