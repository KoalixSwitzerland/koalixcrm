# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import gettext as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline


class GenericProjectLink(models.Model):
    id = models.BigAutoField(primary_key=True)
    project = models.ForeignKey("Project",
                                on_delete=models.CASCADE,
                                verbose_name=_('Project'),
                                blank=False,
                                null=False)
    project_link_type = models.ForeignKey("ProjectLinkType",
                                          on_delete=models.CASCADE,
                                          verbose_name=_('Project Link Type'),
                                          blank=True,
                                          null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    generic_crm_object = GenericForeignKey('content_type',
                                           'object_id')
    date_of_creation = models.DateTimeField(verbose_name=_("Created at"),
                                            auto_now_add=True)
    last_modified_by = models.ForeignKey('auth.User',
                                         on_delete=models.CASCADE,
                                         limit_choices_to={'is_staff': True},
                                         verbose_name=_("Last modified by"),
                                         related_name="db_project_link_last_modified")

    def __str__(self):
        return _("Link to") + " " + str(self.project)

    class Meta:
        app_label = "crm"
        verbose_name = _('Project Link')
        verbose_name_plural = _('Project Links')


class GenericLinkInlineAdminView(admin.TabularInline):
    model = GenericProjectLink
    readonly_fields = ('project_link_type',
                       'content_type',
                       'object_id',
                       'date_of_creation',
                       'last_modified_by')
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class InlineGenericProjectLink(GenericTabularInline):
    model = GenericProjectLink
    readonly_fields = ('project_link_type',
                       'content_type',
                       'object_id',
                       'date_of_creation',
                       'last_modified_by')
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
