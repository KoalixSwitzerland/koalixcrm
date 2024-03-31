# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import gettext as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib import admin


class GenericTaskLink(models.Model):
    id = models.BigAutoField(primary_key=True)
    task = models.ForeignKey("Task",
                             on_delete=models.CASCADE,
                             verbose_name=_('Task'),
                             blank=False, null=False)
    task_link_type = models.ForeignKey("TaskLinkType",
                                       on_delete=models.CASCADE,
                                       verbose_name=_('Task Link Type'),
                                       blank=True,
                                       null=True)
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    generic_crm_object = GenericForeignKey('content_type',
                                           'object_id')
    date_of_creation = models.DateTimeField(verbose_name=_("Created at"),
                                            auto_now_add=True)
    last_modified_by = models.ForeignKey('auth.User',
                                         on_delete=models.CASCADE,
                                         limit_choices_to={'is_staff': True},
                                         verbose_name=_("Last modified by"),
                                         related_name="db_task_link_last_modified")

    def __str__(self):
        return str(self.id)

    class Meta:
        app_label = "crm"
        verbose_name = _('Task Link')
        verbose_name_plural = _('Task Links')


class InlineGenericTaskLink(admin.TabularInline):
    model = GenericTaskLink
    readonly_fields = ('task_link_type',
                       'content_type',
                       'object_id',
                       'date_of_creation',
                       'last_modified_by')
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
