# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _


class WorkCategory(models.Model):
    title = models.CharField(verbose_name=_("Title"), max_length=300, blank=False, null=False)
    description = models.TextField(verbose_name=_("Text"), blank=True, null=True)

    class Meta:
        app_label = "crm"
        verbose_name = _('Work Category')
        verbose_name_plural = _('Work Category')


