# -*- coding: utf-8 -*-
"""Admin registration for ServiceAccountGrant — superuser-only, by design.

koalixcrm#432. Every permission hook is a bare ``request.user.is_superuser``
check, deliberately independent of ``Group.permissions``: a non-superuser
staff user, however broad their other permissions, must neither see this
model in the admin index nor reach it via a direct URL. Granting unrestricted
actor status is not something an ordinary "change" permission should ever
confer.
"""
from django.contrib import admin
from django.http import HttpRequest

from koalixcrm.core.models.service_account_grant import ServiceAccountGrant


@admin.register(ServiceAccountGrant)
class ServiceAccountGrantAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at']
    raw_id_fields = ['user']

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
