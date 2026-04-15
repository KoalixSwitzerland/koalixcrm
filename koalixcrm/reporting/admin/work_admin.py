# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import gettext as _
from django.contrib import messages
from koalixcrm.reporting.models.work import Work


class WorkAdminView(admin.ModelAdmin):
    list_display = ('link_to_work',
                    'human_resource',
                    'task',
                    'get_short_description',
                    'date',
                    'reporting_period',
                    'effort_as_string',
                    'confirmed')

    list_filter = ('task', 'date')
    ordering = ('-id',)

    fieldsets = (
        (_('Work'), {
            'fields': ('human_resource',
                       'date',
                       'start_time',
                       'stop_time',
                       'worked_hours',
                       'short_description',
                       'description',
                       'task',
                       'reporting_period')
        }),
    )
    save_as = True

    actions = ['delete_work', ]

    def delete_work(self, request, queryset):
        for obj in queryset:
            if obj.reporting_period.status.is_done:
                self.message_user(request, _("Delete is not allowed because the work"
                                             " is used in a reporting period which is marked "
                                             "'as done'"),
                                  level=messages.ERROR)
            else:
                obj.delete()

    delete_work.short_description = _("Delete Selected Work")


class WorkInlineAdminView(admin.TabularInline):
    model = Work
    readonly_fields = ('link_to_work',
                       'get_short_description',
                       'human_resource',
                       'date',
                       'effort_as_string',
                       'confirmed',
                       'task',
                       'reporting_period',)
    fieldsets = (
        (_('Work'), {
            'fields': ('link_to_work',
                       'get_short_description',
                       'human_resource',
                       'date',
                       'effort_as_string',
                       'confirmed',
                       'task',
                       'reporting_period',)
        }),
    )
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
