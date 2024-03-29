# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import gettext as _
from django.contrib import admin
from rest_framework import serializers


class AgreementStatus(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name=_("Title"),
                             max_length=250,
                             blank=False,
                             null=False)
    description = models.TextField(verbose_name=_("Text"),
                                   blank=True,
                                   null=True)
    is_agreed = models.BooleanField(verbose_name=_("Status represents agreement exists"),)

    class Meta:
        app_label = "crm"
        verbose_name = _('Agreement Status')
        verbose_name_plural = _('Agreement Status')

    def __str__(self):
        return str(self.id) + " " + str(self.title)


class AgreementStatusAdminView(admin.ModelAdmin):
    list_display = ('id',
                    'title',
                    'description',
                    'is_agreed')

    fieldsets = (
        (_('Agreement Status'), {
            'fields': ('title',
                       'description',
                       'is_agreed')
        }),
    )
    save_as = True


class AgreementStatusJSONSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AgreementStatus
        fields = ('id',
                  'title',
                  'description',)
