# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import gettext as _


class TaskLinkType(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name=_("Title"), max_length=300, blank=False, null=False)
    description = models.TextField(verbose_name=_("Text"), blank=True, null=True)

    class Meta:
        app_label = "reporting"
        db_table = "crm_tasklinktype"
        verbose_name = _('Task Link Type')
        verbose_name_plural = _('Task Link Type')

    def __str__(self):
        return str(self.id) + " " + str(self.title)
