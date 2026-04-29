# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Any

from django.contrib import admin, messages
from django.db.models import Model, QuerySet
from django.forms import ModelForm
from django.http import HttpRequest
from django.utils.translation import gettext as _

from koalixcrm.core.admin.workspace_scoped_admin import WorkspaceScopedModelAdmin
from koalixcrm.reporting.admin.work_admin import WorkInlineAdminView
from koalixcrm.reporting.models.reporting_period import (
    ReportingPeriod,
    ReportingPeriodAdminForm,
)


class ReportingPeriodAdmin(WorkspaceScopedModelAdmin, admin.ModelAdmin):
    form = ReportingPeriodAdminForm
    list_display = ('id',
                    'project',
                    'title',
                    'begin',
                    'end',
                    'status')

    list_display_links = ('id',)
    ordering = ('-id',)

    fieldsets = (
        (_('ReportingPeriod'), {
            'fields': ('project',
                       'title',
                       'begin',
                       'end',
                       'status')
        }),
    )

    inlines = [WorkInlineAdminView, ]
    actions = ['create_report_pdf', ]

    def save_model(self, request: HttpRequest, obj: Model, form: ModelForm, change: bool) -> None:
        if change:
            obj.last_modified_by = request.user
        else:
            obj.last_modified_by = request.user
            obj.staff = request.user
        super().save_model(request, obj, form, change)

    def create_report_pdf(self, request: HttpRequest, queryset: QuerySet[Any]) -> None:
        """Enqueue an async PDFExportProcess per selected reporting period.
        The Java worker fetches ``/reporting-periods/<id>/report-data/``
        for the period-scoped snapshot, then renders + uploads the PDF.
        """
        from koalixcrm.core.models.pdf_export_process import PDFExportProcess
        from koalixcrm.core.models.workspace import Workspace
        workspace = getattr(request, 'active_workspace', None) or Workspace.objects.first()
        queued = 0
        for obj in queryset:
            template_set = getattr(
                obj.project.default_template_set, 'monthly_project_summary_template', None
            )
            if not template_set:
                self.message_user(
                    request,
                    _("Monthly project summary template missing on project %(project)s") % {
                        'project': obj.project
                    },
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
                _("%(count)d reporting-period report job(s) queued.") % {'count': queued},
                level=messages.SUCCESS,
            )

    create_report_pdf.short_description = _("Create Report PDF")


class ReportingPeriodInlineAdminView(admin.TabularInline):
    model = ReportingPeriod
    fieldsets = (
        (_('ReportingPeriod'), {
            'fields': ('project',
                       'title',
                       'begin',
                       'end',
                       'status')
        }),
    )

    def has_add_permission(self, request: HttpRequest, obj: Any = None) -> bool:
        return False

    def has_delete_permission(self, request: HttpRequest, obj: Any = None) -> bool:
        return False
