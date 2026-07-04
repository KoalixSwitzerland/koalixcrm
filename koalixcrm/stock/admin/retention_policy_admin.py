# -*- coding: utf-8 -*-
"""
RetentionPolicyAdmin for koalixcrm stock
"""
from __future__ import annotations

from django.contrib import admin

from koalixcrm.core.admin.workspace_scoped_admin import WorkspaceScopedModelAdmin
from koalixcrm.stock.models.retention_policy import RetentionPolicy


@admin.register(RetentionPolicy)
class RetentionPolicyAdmin(WorkspaceScopedModelAdmin, admin.ModelAdmin):
    list_display = ('workspace', 'serial_unit_retention_floor_days')
    list_filter = ('workspace',)
