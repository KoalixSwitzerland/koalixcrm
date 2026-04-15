# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import gettext as _
from koalixcrm.reporting.models.task import Task
from koalixcrm.reporting.admin.agreement_admin import AgreementInlineAdminView
from koalixcrm.reporting.admin.estimation_admin import EstimationInlineAdminView
from koalixcrm.reporting.admin.generic_task_link_admin import InlineGenericTaskLink
from koalixcrm.reporting.admin.work_admin import WorkInlineAdminView


class TaskAdminView(admin.ModelAdmin):
    list_display = ('link_to_task',
                    'planned_start',
                    'planned_end',
                    'project',
                    'status',
                    'last_status_change',
                    'planned_duration',
                    'planned_total_costs',
                    'effective_duration',
                    'effective_effort_overall',
                    'effective_costs_confirmed',
                    'effective_costs_not_confirmed')
    list_display_links = ('link_to_task',)
    list_filter = ('project',)
    ordering = ('-id',)

    fieldsets = (
        (_('Work'), {
            'fields': ('title',
                       'project',
                       'description',
                       'status')
        }),
    )
    save_as = True
    inlines = [AgreementInlineAdminView,
               EstimationInlineAdminView,
               InlineGenericTaskLink,
               WorkInlineAdminView]


class TaskInlineAdminView(admin.TabularInline):
    model = Task
    readonly_fields = ('link_to_task',
                       'last_status_change',
                       'planned_start',
                       'planned_end',
                       'planned_duration',
                       'planned_total_costs',
                       'effective_duration',
                       'effective_effort_overall',
                       'effective_costs_confirmed',
                       'effective_costs_not_confirmed')
    fieldsets = (
        (_('Task'), {
            'fields': ('link_to_task',
                       'title',
                       'planned_start',
                       'planned_end',
                       'status',
                       'last_status_change',
                       'planned_duration',
                       'planned_total_costs',
                       'effective_duration',
                       'effective_effort_overall',
                       'effective_costs_confirmed',
                       'effective_costs_not_confirmed')
        }),
    )
    extra = 1

    def has_add_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return False
