# -*- coding: utf-8 -*-

from datetime import *
from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext as _
from koalixcrm.crm.documents.pdfexport import PDFExport
from rest_framework import serializers


class ReportingPeriod(models.Model):
    """The reporting period is referred in the work, in the expenses and purchase orders, it is used as a
       supporting object to generate project reports"""
    project = models.ForeignKey("Project",
                                verbose_name=_('Project'),
                                blank=False, null=False)
    title = models.CharField(max_length=200,
                             verbose_name=_("Title"),
                             blank=False, null=False)  # For example "March 2018", "1st Quarter 2019"
    begin = models.DateField(verbose_name=_("Begin"),
                             blank=False, null=False)
    end = models.DateField(verbose_name=_("End"),
                           blank=False, null=False)
    status = models.ForeignKey("ReportingPeriodStatus",
                               verbose_name=_('Status Reporting Period'),
                               blank=False, null=False)

    @staticmethod
    def get_current_valid_reporting_period():
        """Returns the accounting period that is currently valid. Valid is an accounting_period when the current date
          lies between begin and end of the accounting_period

        Args:
          no arguments

        Returns:
          accounting_period (AccoutingPeriod)

        Raises:
          AccountingPeriodNotFound when there is no valid accounting Period"""
        current_valid_accounting_period = None
        for accounting_period in AccountingPeriod.objects.all():
            if accounting_period.begin < date.today() and accounting_period.end > date.today():
                return accounting_period
        if not current_valid_accounting_period:
            raise AccountingPeriodNotFound()

    @staticmethod
    def get_all_prior_reporting_periods(target_reporting_period):
        """Returns the reporting period that is currently valid. Valid is a reporting period when the current date
          lies between begin and end of the reporting period

        Args:
          no arguments

        Returns:
          reporting_period (List of AccoutingPeriod)

        Raises:
          AccountingPeriodNotFound when there is no valid accounting Period"""
        accounting_periods = []
        for accounting_period in AccountingPeriod.objects.all():
            if accounting_period.end < target_accounting_period.begin:
                accounting_periods.append(accounting_period)
        if accounting_periods == []:
            raise AccountingPeriodNotFound("Accounting Period does not exist")
        return accounting_periods

    def create_pdf(self, template_set, printed_by):
        self.last_print_date = datetime.now()
        self.save()
        return PDFExport.create_pdf(self, template_set, printed_by)

    def get_template_set(self):
        return self.project.get_template_set()

    def get_fop_config_file(self, template_set):
        return self.project.get_fop_config_file()

    def get_xsl_file(self, template_set):
        return self.project.get_xsl_file()

    def serialize_to_xml(self):
        from koalixcrm.djangoUserExtension.models import UserExtension
        objects = [self, ]
        objects += UserExtension.objects_to_serialize(self, self.project_manager)
        main_xml = PDFExport.write_xml(objects)
        project_xml = self.project.serialize_to_xml(reporting_period=self)
        main_xml = PDFExport.merge_xml(main_xml, project_xml)
        return main_xml

    def __str__(self):
        return str(self.id)+" "+self.title

    class Meta:
        app_label = "crm"
        verbose_name = _('Reporting Period')
        verbose_name_plural = _('Reporting Periods')


class OptionReportingPeriod(admin.ModelAdmin):
    list_display = ('id',
                    'project',
                    'title',
                    'begin',
                    'end')

    list_display_links = ('id',)
    ordering = ('-id',)

    fieldsets = (
        (_('ReportingPeriod'), {
            'fields': ('project',
                       'title',
                       'begin',
                       'end')
        }),
    )

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
                                                ("/admin/crm/"+obj.__class__.__name__.lower()+"/"),
                                                obj.default_template_set.monthly_project_summary_template)
            return response

    create_report_pdf.short_description = _("Create Report PDF")


class InlineReportingPeriod(admin.TabularInline):
    model = ReportingPeriod
    fieldsets = (
        (_('ReportingPeriod'), {
            'fields': ('project',
                       'title',
                       'begin',
                       'end')
        }),
    )
    extra = 0

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ProjectJSONSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ReportingPeriod
        fields = ('id',
                  'project',
                  'title',
                  'begin',
                  'end')