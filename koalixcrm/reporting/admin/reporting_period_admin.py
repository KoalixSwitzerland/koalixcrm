# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import gettext as _
from koalixcrm.reporting.models.reporting_period import ReportingPeriod, ReportingPeriodAdminForm
from koalixcrm.reporting.admin.work_admin import WorkInlineAdminView


class ReportingPeriodAdmin(admin.ModelAdmin):
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

    def save_model(self, request, obj, form, change):
        if change:
            obj.last_modified_by = request.user
        else:
            obj.last_modified_by = request.user
            obj.staff = request.user
        obj.save()

    def create_report_pdf(self, request, queryset):
        from koalixcrm.core.views.pdfexport import PDFExportView
        for obj in queryset:
            response = PDFExportView.export_pdf(self,
                                                request,
                                                obj,
                                                ("/admin/reporting/"+obj.__class__.__name__.lower()+"/"),
                                                obj.project.default_template_set.monthly_project_summary_template)
            return response

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

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
