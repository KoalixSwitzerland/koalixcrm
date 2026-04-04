# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import gettext as _
from koalixcrm.reporting.models.project import Project
from koalixcrm.reporting.admin.task_admin import TaskInlineAdminView
from koalixcrm.reporting.admin.generic_project_link_admin import GenericLinkInlineAdminView
from koalixcrm.reporting.admin.reporting_period_admin import ReportingPeriodInlineAdminView


class ProjectAdminView(admin.ModelAdmin):
    list_display = ('id',
                    'project_name',
                    'project_manager',
                    'project_status',
                    'planned_total_costs',
                    'planned_duration',
                    'effective_duration',
                    'effective_effort',
                    'effective_costs_confirmed',
                    'effective_costs_not_confirmed'
                    )

    list_display_links = ('id',)
    ordering = ('-id',)

    fieldsets = (
        (_('Project'), {
            'fields': ('project_name',
                       'description',
                       'project_status',
                       'project_manager',
                       'default_currency',
                       'default_template_set',)
        }),
    )

    inlines = [TaskInlineAdminView,
               GenericLinkInlineAdminView,
               ReportingPeriodInlineAdminView]
    actions = ['create_report_pdf', ]

    def save_model(self, request, obj, form, change):
        if change:
            obj.last_modified_by = request.user
        else:
            obj.last_modified_by = request.user
            obj.staff = request.user
        obj.save()

    def create_report_pdf(self, request, queryset):
        from koalixcrm.crm.views.pdfexport import PDFExportView
        for obj in queryset:
            response = PDFExportView.export_pdf(self,
                                                request,
                                                obj,
                                                ("/admin/reporting/"+obj.__class__.__name__.lower()+"/"),
                                                obj.default_template_set.monthly_project_summary_template)
            return response

    create_report_pdf.short_description = _("Create Report PDF")


class ProjectInlineAdminView(admin.TabularInline):
    model = Project
    readonly_fields = ('link_to_project',
                       'project_name',
                       'description',
                       'project_status',
                       'project_manager',
                       'default_template_set')
    fieldsets = (
        (_('Project'), {
            'fields': ('link_to_project',
                       'project_name',
                       'description',
                       'project_status',
                       'project_manager',
                       'default_template_set')
        }),
    )
    extra = 0

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
