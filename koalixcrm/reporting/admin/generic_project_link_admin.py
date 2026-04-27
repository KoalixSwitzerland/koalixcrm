# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from koalixcrm.reporting.models.generic_project_link import GenericProjectLink


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


class InlineGenericProjectLinkAdmin(GenericTabularInline):
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
