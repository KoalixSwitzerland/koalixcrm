# -*- coding: utf-8 -*-

from datetime import *
from django.db import models
from django.contrib import admin
from django.utils.translation import gettext as _
from koalixcrm.crm.documents.pdf_export import PDFExport
from koalixcrm.crm.exceptions import ReportingPeriodNotFound
from koalixcrm.crm.reporting.work import WorkInlineAdminView
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.forms import ModelForm


class ReportingPeriod(models.Model):
    """The reporting period is referred in the work, in the expenses and purchase orders, it is used as a
       supporting object to generate project reports"""
    id = models.BigAutoField(primary_key=True)
    project = models.ForeignKey("Project",
                                on_delete=models.CASCADE,
                                verbose_name=_("Project"),
                                blank=False,
                                null=False)
    title = models.CharField(max_length=200,
                             verbose_name=_("Title"),
                             blank=False,
                             null=False)  # For example "March 2018", "1st Quarter 2019"
    begin = models.DateField(verbose_name=_("Begin"),
                             blank=False,
                             null=False)
    end = models.DateField(verbose_name=_("End"),
                           blank=False,
                           null=False)
    status = models.ForeignKey("ReportingPeriodStatus",
                               on_delete=models.CASCADE,
                               verbose_name=_("Reporting Period Status"),
                               blank=True,
                               null=True)

    @staticmethod
    def get_reporting_period(project, search_date):
        """Returns the reporting period that is currently valid. Valid is a reporting period when the provided date
          lies between begin and end of the reporting period

        Args:
          no arguments

        Returns:
          reporting_period (ReportPeriod)

        Raises:
          ReportPeriodNotFound when there is no valid reporting Period"""
        current_valid_reporting_period = None
        for reporting_period in ReportingPeriod.objects.filter(project=project):
            if reporting_period.begin <= search_date <= reporting_period.end:
                return reporting_period
        if not current_valid_reporting_period:
            raise ReportingPeriodNotFound("Reporting Period does not exist")

    @staticmethod
    def get_latest_reporting_period(project):
        """Returns the latest reporting period

        Args:
          no arguments

        Returns:
          reporting_period (ReportPeriod)

        Raises:
          ReportPeriodNotFound when there is no valid reporting Period"""
        latest_reporting_period = None
        reporting_periods = ReportingPeriod.objects.filter(project=project)
        for reporting_period in reporting_periods:
            if latest_reporting_period is None:
                latest_reporting_period = reporting_period
            else:
                if latest_reporting_period.end <= reporting_period.begin:
                    latest_reporting_period = reporting_period
        if not latest_reporting_period:
            raise ReportingPeriodNotFound("Reporting Period does not exist")
        return latest_reporting_period

    @staticmethod
    def get_predecessor(target_reporting_period, project):
        """Returns the reporting period which was valid right before the provided target_reporting_period

        Args:
          no arguments

        Returns:
          predecessor_reporting_period (ReportPeriod)

        Raises:
          ReportPeriodNotFound when there is no valid reporting Period"""
        predecessor_reporting_period = None
        reporting_periods = ReportingPeriod.objects.filter(project=project)
        for reporting_period in reporting_periods:
            if reporting_period.end <= target_reporting_period.begin and\
                    predecessor_reporting_period is None:
                predecessor_reporting_period = reporting_period
            elif reporting_period.end <= target_reporting_period.begin and \
                    predecessor_reporting_period.end <= reporting_period.begin:
                predecessor_reporting_period = reporting_period
        if predecessor_reporting_period is None:
            raise ReportingPeriodNotFound("Reporting Period does not exist")
        return predecessor_reporting_period

    @staticmethod
    def get_all_predecessors(target_reporting_period, project):
        """Returns all reporting periods which have been valid before the provided target_reporting_period

        Args:
          no arguments

        Returns:
          predecessor_reporting_periods[] (Array of ReportPeriod)

        Raises:
          ReportPeriodNotFound when there is no valid reporting Period"""
        predecessor_reporting_periods = list()
        reporting_periods = ReportingPeriod.objects.filter(project=project)
        for reporting_period in reporting_periods:
            if reporting_period.end <= target_reporting_period.begin:
                predecessor_reporting_periods.append(reporting_period)
        return predecessor_reporting_periods

    def is_reporting_allowed(self):
        """Returns True when the reporting period is available for reporting,
        Returns False when the reporting period is not available for reporting,
        The decision whether the reporting period is available for reporting is purely depending
        on the reporting_period_status. When the status is done, the reporting period is not longer
        available for reporting. In all other cases the reporting is allowed.

        Args:
          no arguments

        Returns:
          allowed (Boolean)

        Raises:
           when there is no valid reporting Period"""
        if self.status:
            if self.status.is_done:
                allowed = False
            else:
                allowed = True
        else:
            allowed = False
        return allowed

    def create_pdf(self, template_set, printed_by):
        self.last_print_date = datetime.now()
        self.save()
        return PDFExport.create_pdf(self, template_set, printed_by)

    def get_template_set(self):
        return self.project.get_template_set()

    def get_fop_config_file(self, template_set):
        return self.project.get_fop_config_file(template_set=None)

    def get_xsl_file(self, template_set):
        return self.project.get_xsl_file(template_set=None)

    def serialize_to_xml(self):
        objects = [self, ]
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


class ReportingPeriodAdminForm(ModelForm):
    def clean(self):
        """Check that the begin of the new reporting period is not located within an existing
        reporting period, Checks that the begin date earlier than the end date. Verify that in case there
        is already a predecessor or a successor reporting period, the reporting periods are in direct contact
        with each other"""
        cleaned_data = super().clean()
        project = cleaned_data['project']
        end = cleaned_data['end']
        begin = cleaned_data['begin']
        reporting_periods = ReportingPeriod.objects.filter(project=project)
        for reporting_period in reporting_periods:
            if reporting_period.pk != self.instance.pk:
                if (begin < reporting_period.end) and (begin > reporting_period.begin):
                    raise ValidationError('The Reporting Period overlaps with an existing '
                                          'Reporting Period within the same project')
                if (end < reporting_period.end) and (end > reporting_period.begin):
                    raise ValidationError('The Reporting Period overlaps with an existing '
                                          'Reporting Period within the same project')
        if end < begin:
            raise ValidationError('Begin date must be earlier than end date')
        if len(reporting_periods) > 1:
            reporting_periods_direct_predecessor = ReportingPeriod.objects.filter(project=project,
                                                                                  end=begin-timedelta(1))
            reporting_periods_direct_successor = ReportingPeriod.objects.filter(project=project,
                                                                                begin=end+timedelta(1))
            if (len(reporting_periods_direct_predecessor) == 0) and (len(reporting_periods_direct_successor) == 0):
                raise ValidationError('The new reporting period has to be directly following a previous reporting '
                                      'period or it has to be directly before the following reporting period')


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
        from koalixcrm.crm.views.pdfexport import PDFExportView
        for obj in queryset:
            response = PDFExportView.export_pdf(self,
                                                request,
                                                obj,
                                                ("/admin/crm/"+obj.__class__.__name__.lower()+"/"),
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


class ProjectJSONSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ReportingPeriod
        fields = ('id',
                  'project',
                  'title',
                  'begin',
                  'end')
