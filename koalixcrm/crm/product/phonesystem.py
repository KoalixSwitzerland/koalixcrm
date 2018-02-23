# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _

class PhoneSystem(models.Model):
    system_model = models.CharField(verbose_name=_("Model"), max_length=200, blank=True, null=True)
    year =  models.IntegerField(verbose_name=_("Year of installation"), blank=True, null=True)
    n_phones_ana = models.IntegerField(verbose_name=_("Analog phones"), blank=True, null=True)
    n_phones_dig = models.IntegerField(verbose_name=_("Digital phones"), blank=True, null=True)
    n_ext_lines = models.IntegerField(verbose_name=_("External lines"), blank=True, null=True)
    
    class Meta:
        app_label = "crm"
        verbose_name = _('Phone System')
        verbose_name_plural = _('Phone System')



