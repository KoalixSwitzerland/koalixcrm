# -*- coding: utf-8 -*-
from django.contrib import admin
from koalixcrm.djangoUserExtension.models.user_extension import (
    UserExtension,
    OptionUserExtension,
    UserAddressAssignment,
    UserPhoneAssignment,
    UserEmailAssignment,
)
from koalixcrm.djangoUserExtension.models.template_set import TemplateSet, OptionTemplateSet

admin.site.register(UserExtension, OptionUserExtension)
admin.site.register(TemplateSet, OptionTemplateSet)


@admin.register(UserAddressAssignment)
class UserAddressAssignmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'address', 'purpose', 'is_primary', 'valid_from', 'valid_to')
    list_filter = ('purpose', 'is_primary', 'workspace')
    raw_id_fields = ('user', 'address')


@admin.register(UserPhoneAssignment)
class UserPhoneAssignmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone_number', 'purpose', 'is_primary', 'valid_from', 'valid_to')
    list_filter = ('purpose', 'is_primary', 'workspace')
    raw_id_fields = ('user', 'phone_number')


@admin.register(UserEmailAssignment)
class UserEmailAssignmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'email', 'purpose', 'is_primary', 'valid_from', 'valid_to')
    list_filter = ('purpose', 'is_primary', 'workspace')
    raw_id_fields = ('user', 'email')
