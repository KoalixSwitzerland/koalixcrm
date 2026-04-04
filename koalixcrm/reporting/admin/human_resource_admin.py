# -*- coding: utf-8 -*-

from django.contrib import admin
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
        from koalixcrm.crm.views.create_work_report import create_work_report

        return create_work_report(self, request, queryset)

    create_work_report_pdf.short_description = _("Work Report PDF")

    save_as = True
    actions = [create_work_report_pdf]
    inlines = [ResourcePriceInlineAdminView]
