# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext as _


class CustomerGroup(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return str(self.id) + ' ' + self.name

    class Meta:
        app_label = "crm"
        verbose_name = _('Customer Group')
        verbose_name_plural = _('Customer Groups')


class OptionCustomerGroup(admin.ModelAdmin):
    list_display = ('id', 'name')
    fieldsets = (('', {'fields': ('name',)}),)
    allow_add = True