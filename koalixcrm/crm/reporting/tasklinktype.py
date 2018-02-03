# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _


class TaskLinkType(models.Model):
    title = models.CharField(verbose_name=_("Title"), max_length=300, blank=False, null=False)
    description = models.TextField(verbose_name=_("Text"), blank=True, null=True)

    class Meta:
        app_label = "crm"
        verbose_name = _('Task Link Type')
        verbose_name_plural = _('Task Link Type')