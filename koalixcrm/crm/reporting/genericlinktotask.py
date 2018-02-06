# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.contenttypes.fields import GenericForeignKey


class GenericTaskLink(models.Model):
    task = models.ForeignKey("Task", verbose_name=_('Task'), blank=False, null=False)
    task_link_type = models.ForeignKey("TaskLinkType", verbose_name=_('Task Link Type'), blank=False, null=False)
    generic_crm_object = GenericForeignKey()

    def __str__(self):
        return _("Task Link") + " ID: " + str(self.id)

    class Meta:
        app_label = "crm"
        verbose_name = _('Task Link')
        verbose_name_plural = _('Task Links')

