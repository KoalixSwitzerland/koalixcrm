# -*- coding: utf-8 -*-

from django.contrib import admin, messages
from django.utils.translation import gettext as _

from koalixcrm.reporting.admin.generic_project_link_admin import (
    GenericLinkInlineAdminView,
)
from koalixcrm.reporting.admin.reporting_period_admin import (
    ReportingPeriodInlineAdminView,
)
from koalixcrm.reporting.admin.task_admin import TaskInlineAdminView
from koalixcrm.reporting.models.project import Project


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
        """Enqueue an async PDFExportProcess per selected project. The Java
        pdf-export-service picks the message up from SQS, fetches the JSON
        snapshot from ``/projects/<id>/report-data/``, renders the PDF, and
        writes the result URL back onto the process row. Watch the PDF
        Export Processes admin for status.
        """
        from koalixcrm.core.models.pdf_export_process import PDFExportProcess
        from koalixcrm.core.models.workspace import Workspace
        workspace = getattr(request, 'active_workspace', None) or Workspace.objects.first()
        queued = 0
        for obj in queryset:
            template_set = getattr(obj.default_template_set, 'monthly_project_summary_template', None)
            if not template_set:
                self.message_user(
                    request,
                    _("Monthly project summary template missing for %(project)s") % {'project': obj},
                    level=messages.ERROR,
                )
                continue
            PDFExportProcess.objects.create(
                workspace=workspace,
                source_model=obj.__class__.__name__,
                source_id=obj.id,
                template_set=template_set,
                triggered_by=request.user,
            )
            queued += 1
        if queued:
            self.message_user(
                request,
                _("%(count)d project report job(s) queued.") % {'count': queued},
                level=messages.SUCCESS,
            )

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
