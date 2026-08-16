# -*- coding: utf-8 -*-
"""ServiceProfile admin for koalixcrm products (ADR-0007, REQ-0016)."""
from __future__ import annotations

from django.contrib import admin

from koalixcrm.core.admin.workspace_scoped_admin import WorkspaceScopedModelAdmin
from koalixcrm.products.models.service_profile import ServiceProfile


class ServiceProfileInlineAdmin(admin.StackedInline):
    model = ServiceProfile
    fk_name = "product"
    extra = 0
    max_num = 1
    classes = ['collapse']
    fields = ('billing_model', 'default_duration', 'deliverable', 'sla_reference')
    allow_add = True


@admin.register(ServiceProfile)
class ServiceProfileAdmin(WorkspaceScopedModelAdmin, admin.ModelAdmin):
    list_display = ('product', 'billing_model', 'default_duration')
    list_filter = ('workspace', 'billing_model')
    search_fields = ('product__title', 'deliverable')
