# -*- coding: utf-8 -*-
"""Admin registration for OidcTenant — superuser-only, by design.

koalixcrm#430. Registering a tenant row is what activates OIDC group
synchronisation for an issuer, so it is an administrative act with the same
weight as granting a service account: gated on ``is_superuser`` rather than
on a model permission a role projection could hand out.
"""
from django.contrib import admin
from django.http import HttpRequest

from koalixcrm.core.models.oidc_tenant import OidcTenant


@admin.register(OidcTenant)
class OidcTenantAdmin(admin.ModelAdmin):
    list_display = ['id', 'alias', 'issuer', 'display_name']
    search_fields = ['alias', 'issuer', 'display_name']
    ordering = ['alias']

    def has_module_permission(self, request: HttpRequest) -> bool:
        return bool(getattr(request.user, 'is_superuser', False))

    def has_view_permission(self, request: HttpRequest, obj: object = None) -> bool:
        return bool(getattr(request.user, 'is_superuser', False))

    def has_add_permission(self, request: HttpRequest) -> bool:
        return bool(getattr(request.user, 'is_superuser', False))

    def has_change_permission(self, request: HttpRequest, obj: object = None) -> bool:
        return bool(getattr(request.user, 'is_superuser', False))

    def has_delete_permission(self, request: HttpRequest, obj: object = None) -> bool:
        return bool(getattr(request.user, 'is_superuser', False))
