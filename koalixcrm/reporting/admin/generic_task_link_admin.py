# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Any

from django.contrib import admin
from django.http import HttpRequest

from koalixcrm.reporting.models.generic_task_link import GenericTaskLink


class InlineGenericTaskLink(admin.TabularInline):
    model = GenericTaskLink
    readonly_fields = ('task_link_type',
                       'content_type',
                       'object_id',
                       'date_of_creation',
                       'last_modified_by')
    extra = 0

    def has_add_permission(self, request: HttpRequest, obj: Any = None) -> bool:
        return False

    def has_delete_permission(self, request: HttpRequest, obj: Any = None) -> bool:
        return False
