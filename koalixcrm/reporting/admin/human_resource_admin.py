# -*- coding: utf-8 -*-

from django.contrib import admin, messages
from django.utils.translation import gettext as _

from koalixcrm.reporting.admin.resource_price_admin import ResourcePriceInlineAdminView


class HumanResourceAdminView(admin.ModelAdmin):
    list_display = ('id',
                    'user',
                    'resource_manager',
                    'resource_type')
    list_display_links = ('id',
                          'user')
    list_filter = ('user',)
    ordering = ('id',)
    search_fields = ('id',
                     'user')
    fieldsets = (
        (_('Basics'), {
            'fields': ('user',
                       'resource_manager',
                       'resource_type')
        }),
    )

    def create_work_report_pdf(self, request, queryset):
        """Enqueue an async PDFExportProcess per selected human resource. The
        Java worker fetches ``/human-resources/<id>/work-report-data/`` and
        renders the work_report XSL.

        TODO(#404): re-introduce the date-range form once
        ``PDFExportProcess`` has a ``params`` JSONField — until then the
        worker hits the endpoint without query args and the report covers
        the trailing 60 days (the legacy default).
        """
        from koalixcrm.core.models.pdf_export_process import PDFExportProcess
        from koalixcrm.core.models.workspace import Workspace
        workspace = getattr(request, 'active_workspace', None) or Workspace.objects.first()
        queued = 0
        for obj in queryset:
            template_set = getattr(
                obj.user.default_template_set, 'work_report_template', None
            )
            if not template_set:
                self.message_user(
                    request,
                    _("Work report template missing for %(hr)s") % {'hr': obj},
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
                _("%(count)d work report job(s) queued.") % {'count': queued},
                level=messages.SUCCESS,
            )

    create_work_report_pdf.short_description = _("Work Report PDF")

    save_as = True
    actions = [create_work_report_pdf]
    inlines = [ResourcePriceInlineAdminView]
