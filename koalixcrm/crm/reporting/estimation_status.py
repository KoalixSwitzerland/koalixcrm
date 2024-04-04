# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import gettext as _
from django.contrib import admin
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
        app_label = "crm"
        verbose_name = _('Estimation Status')
        verbose_name_plural = _('Estimation Status')

    def __str__(self):
        return str(self.id) + " " + str(self.title)


class EstimationStatusAdminView(admin.ModelAdmin):
    list_display = ('id',
                    'title',
                    'description',
                    'is_obsolete')

    fieldsets = (
        (_('Agreement Status'), {
            'fields': ('title',
                       'description',
                       'is_obsolete')
        }),
    )
    save_as = True


class EstimationStatusJSONSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EstimationStatus
        fields = ('id',
                  'title',
                  'description',)
