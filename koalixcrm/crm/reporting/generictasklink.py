# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.contenttypes.models import ContentType


class GenericTaskLink(models.Model):
    task = models.ForeignKey("Task", verbose_name=_('Task'), blank=False, null=False)
    task_link_type = models.ForeignKey("TaskLinkType", verbose_name=_('Task Link Type'), blank=False, null=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    generic_crm_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return _("Task Link")

    class Meta:
        app_label = "crm"
        verbose_name = _('Task Link')
        verbose_name_plural = _('Task Links')


class InlineGenericTaskLink(GenericTabularInline):
    model = GenericTaskLink
    extra = 1