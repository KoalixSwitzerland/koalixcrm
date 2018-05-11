# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext as _

from koalixcrm.crm.const.modeltype import *

class Attribute(models.Model):
    code = models.CharField(verbose_name=_("Attribute Code"), max_length=50)
    name = models.CharField(verbose_name=_("Attribute Name"), max_length=200)
    model_type = models.CharField(verbose_name=_("Model Type"), max_length=1, choices=MODELTYPE)

    def __str__(self):
        return str(self.id) + ' ' + self.name
    
    class Meta:
        app_label = "crm"
        verbose_name = _('Attribute')
        verbose_name_plural = _('Attributes')

class AttributeSet(models.Model):
    name = models.CharField(verbose_name=_("Attribute Set"), max_length=50)
    attributes = models.ManyToManyField("Attribute", verbose_name=_('Attributes'), blank=True)

    def __str__(self):
        return str(self.id) + ' ' + self.name
    
    class Meta:
        app_label = "crm"
        verbose_name = _('Attribute Set')
        verbose_name_plural = _('Attribute Set')

class OptionAttribute(admin.ModelAdmin):
    list_display = ('code', 'name', 'model_type',)

class OptionAttributeSet(admin.ModelAdmin):
    list_display = ('name',)
    filter_horizontal = ('attributes',)
