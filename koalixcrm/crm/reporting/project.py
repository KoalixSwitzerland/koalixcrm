# -*- coding: utf-8 -*-

from decimal import *
from datetime import *
from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext as _
from django.utils.html import format_html
from koalixcrm.crm.reporting.generic_project_link import GenericLinkInlineAdminView
from koalixcrm.crm.reporting.reporting_period import ReportingPeriodInlineAdminView, ReportingPeriod
from koalixcrm.crm.reporting.task import TaskInlineAdminView
from koalixcrm.crm.documents.pdf_export import PDFExport
from koalixcrm.crm.exceptions import TemplateSetMissingInContract
from koalixcrm.crm.models import Task
from rest_framework import serializers


class Project(models.Model):
    project_manager = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True},
                                        verbose_name=_("Staff"),
                                        related_name="db_rel_project_staff",
                                        blank=True,
                                        null=True)
    project_name = models.CharField(verbose_name=_("Project name"),
                                    max_length=100,
                                    null=True,
                                    blank=True)
    description = models.TextField(verbose_name=_("Description"),
                                   null=True,
                                   blank=True)
    project_status = models.ForeignKey("ProjectStatus",
                                       verbose_name=_('Project Status'),
                                       blank=True,
                                       null=True)
    default_template_set = models.ForeignKey("djangoUserExtension.TemplateSet",
                                             verbose_name=_("Default Template Set"),
                                             null=True,
                                             blank=True)
    default_currency = models.ForeignKey("Currency",
                                         verbose_name=_("Default Currency"),
                                         null=False,
                                         blank=False)
    date_of_creation = models.DateTimeField(verbose_name=_("Created at"),
                                            auto_now_add=True)
    last_modification = models.DateTimeField(verbose_name=_("Last modified"),
                                             auto_now=True)
    last_modified_by = models.ForeignKey('auth.User',
                                         limit_choices_to={'is_staff': True},
                                         verbose_name=_("Last modified by"),
                                         related_name="db_project_last_modified")

    def link_to_project(self):
        if self.id:
            return format_html("<a href='/admin/crm/project/%s' >%s</a>" % (str(self.id), str(self.project_name)))
        else:
            return "Not present"
    link_to_project.short_description = _("Project")

    def create_pdf(self, template_set, printed_by):
        self.last_print_date = datetime.now()
        self.save()
        return PDFExport.create_pdf(self, template_set, printed_by)

    def get_template_set(self):
        if self.default_template_set.monthly_project_summary_template:
            return self.default_template_set.monthly_project_summary_template
        else:
            raise TemplateSetMissingInContract((_("Template Set missing in Project" + str(self))))

    def get_fop_config_file(self, template_set):
        template_set = self.get_template_set()
        return template_set.get_fop_config_file()

    def get_xsl_file(self, template_set):
        template_set = self.get_template_set()
        return template_set.get_xsl_file()

    def get_reporting_period(self, search_date):
        from koalixcrm.crm.reporting.reporting_period import ReportingPeriod
        """Returns the reporting period that is valid. Valid is a reporting period when the provided date
          lies between begin and end of the reporting period

        Args:
          no arguments

        Returns:
          accounting_period (ReportPeriod)

        Raises:
          ReportPeriodNotFound when there is no valid reporting Period"""
        return ReportingPeriod.get_reporting_period(self, search_date)

    def serialize_to_xml(self, **kwargs):
        reporting_period = kwargs.get('reporting_period', None)
        from koalixcrm.djangoUserExtension.models import UserExtension
        objects = [self, ]
        objects += UserExtension.objects_to_serialize(self, self.project_manager)
        main_xml = PDFExport.write_xml(objects)
        for task in Task.objects.filter(project=self.id):
            task_xml = task.serialize_to_xml(reporting_period=reporting_period)
            main_xml = PDFExport.merge_xml(main_xml, task_xml)
        main_xml = PDFExport.append_element_to_pattern(main_xml,
                                                       "object/[@model='crm.project']",
                                                       "Effective_Effort_Overall",
                                                       self.effective_costs(reporting_period=None))
        if reporting_period:
            main_xml = PDFExport.append_element_to_pattern(main_xml,
                                                           "object/[@model='crm.project']",
                                                           "Effective_Effort_InPeriod",
                                                           self.effective_costs(reporting_period=reporting_period))
        main_xml = PDFExport.append_element_to_pattern(main_xml,
                                                       "object/[@model='crm.project']",
                                                       "Planned_Effort",
                                                       self.planned_costs())
        main_xml = PDFExport.append_element_to_pattern(main_xml,
                                                       "object/[@model='crm.project']",
                                                       "Effective_Duration",
                                                       self.effective_duration())
        main_xml = PDFExport.append_element_to_pattern(main_xml,
                                                       "object/[@model='crm.project']",
                                                       "Planned_Duration",
                                                       self.planned_duration())
        return main_xml

    def effective_accumulated_costs(self, reporting_period=None):
        if reporting_period:
            reporting_periods = ReportingPeriod.get_all_predecessors(target_reporting_period=reporting_period,
                                                                     project=self)
        else:
            reporting_periods = ReportingPeriod.objects.filter(project=self.id)
        effective_accumulated_costs = 0
        for single_reporting_period in reporting_periods:
            all_project_tasks = Task.objects.filter(project=self.id)
            for task in all_project_tasks:
                effective_accumulated_costs += float(task.effective_costs(reporting_period=single_reporting_period))
        getcontext().prec = 5
        effective_accumulated_costs = Decimal(effective_accumulated_costs)
        self.default_currency.round(effective_accumulated_costs)
        return effective_accumulated_costs

    effective_accumulated_costs.short_description = _("Effective Accumulated costs")
    effective_accumulated_costs.tags = True

    def effective_costs(self, reporting_period):
        effective_cost = 0
        for task in Task.objects.filter(project=self.id):
            effective_cost += task.effective_costs(reporting_period=reporting_period)
        self.default_currency.round(effective_cost)
        return effective_cost

    def planned_costs(self, reporting_period=None):
        """The function return the planned overall costs

        Args:
        no arguments

        Returns:
        planned costs (String)

        Raises:
        No exceptions planned"""
        planned_effort_accumulated = 0
        all_project_tasks = Task.objects.filter(project=self.id)
        if all_project_tasks:
            for task in all_project_tasks:
                planned_effort_accumulated += task.planned_costs(reporting_period)
        getcontext().prec = 5
        planned_effort_accumulated = Decimal(planned_effort_accumulated)
        self.default_currency.round(planned_effort_accumulated)
        return planned_effort_accumulated
    planned_costs.short_description = _("Planned Costs")
    planned_costs.tags = True

    def effective_start(self):
        """The function return the effective start of a project as a date

        Args:
        no arguments

        Returns:
        effective_start (Date) or None when not yet started

        Raises:
        No exceptions planned"""
        no_tasks_started = True
        all_project_tasks = Task.objects.filter(project=self.id)
        effective_project_start = None
        if len(all_project_tasks) == 0:
            effective_project_start = None
        else:
            for task in all_project_tasks:
                if not effective_project_start:
                    if task.effective_start():
                        effective_project_start = task.effective_start()
                        no_tasks_started = False
                effective_task_start = task.effective_start()
                if effective_task_start:
                    if effective_task_start < effective_project_start:
                        effective_project_start = effective_task_start
            if no_tasks_started:
                effective_project_start = None
        return effective_project_start
    effective_start.short_description = _("Effective Start")
    effective_start.tags = True

    def effective_end(self):
        """The function return the effective end of a project as a date

        Args:
        no arguments

        Returns:
        effective_end (Date) or None when not yet ended

        Raises:
        No exceptions planned"""
        all_tasks_done = True
        all_project_tasks = Task.objects.filter(project=self.id)
        effective_project_end = None
        if len(all_project_tasks) == 0:
            effective_project_end = None
        else:
            i = 0
            for task in all_project_tasks:
                if not effective_project_end:
                    if not task.effective_start():
                        all_tasks_done = False
                        break
                    else:
                        effective_project_end = task.effective_start()
                effective_task_end = task.effective_end()
                if not effective_task_end:
                    all_tasks_done = False
                    break
                elif effective_task_end > effective_project_end:
                    effective_project_end = effective_task_end
                i = i+1
            if not all_tasks_done:
                effective_project_end = None
        return effective_project_end
    effective_end.short_description = _("Effective End")
    effective_end.tags = True

    def effective_duration(self):
        """The function return the effective overall duration of a project as a string in days
        The function is reading the effective_starts and effective_ends of the project and
        subtract them from each other.

        Args:
        no arguments

        Returns:
        duration_in_days or description (String)

        Raises:
        No exceptions planned"""
        effective_end = self.effective_end()
        effective_start = self.effective_start()
        if not effective_start:
            duration_as_string = "Project has not yet started"
        elif not effective_end:
            duration_as_string = "Project has not yet ended"
        else:
            duration_as_date = self.effective_end()-self.effective_start()
            duration_as_string = duration_as_date.days.__str__()
        return duration_as_string
    effective_duration.short_description = _("Effective Duration [dys]")
    effective_duration.tags = True

    def planned_start(self):
        """ The function return planned overall start of a project as a date
        the function finds all tasks within this project and finds the earliest start date.
        when no task is attached the task has which are attached have no start_date set, the
        function returns a None value

        Args:
        no arguments

        Returns:
        planned_end (datetime.Date) or  None

        Raises:
        No exceptions planned"""
        tasks = Task.objects.filter(project=self.id)
        if tasks:
            i = 0
            project_start = None
            for task in tasks:
                if task.planned_start():
                    if i == 0:
                        project_start = task.planned_start()
                    elif task.planned_start() < project_start:
                        project_start = task.planned_start()
                    i += 1
            return project_start
        else:
            return None

    def planned_end(self):
        """T he function return planned overall end of a project as a date
        the function finds all tasks within this project and finds the latest start end_date.
        when no task is attached the task has which are attached have no end_date set, the
        function returns a None value

        Args:
        no arguments

        Returns:
        planned_end (datetime.Date)

        Raises:
        No exceptions planned"""
        tasks = Task.objects.filter(project=self.id)
        if tasks:
            i = 0
            project_end = None
            for task in tasks:
                if task.planned_end():
                    if i == 0:
                        project_end = task.planned_end()
                    elif task.planned_end() > project_end:
                        project_end = task.planned_end()
                    i += 1
                    return project_end
        else:
            return None

    def planned_duration(self):
        """The function return planned overall duration of a project as a string in days

        Args:
        no arguments

        Returns:
        duration_in_days (String)

        Raises:
        No exceptions planned"""
        if (not self.planned_start()) or (not self.planned_end()):
            duration_in_days = "n/a"
        elif self.planned_start() > self.planned_end():
            duration_in_days = "n/a"
        else:
            duration_in_days = (self.planned_end()-self.planned_start()).days.__str__()
        return duration_in_days
    planned_duration.short_description = _("Planned Duration [dys]")
    planned_duration.tags = True

    def get_project_name(self):
        """The function safely returns a project_name even if the values is empty, in such a case
        the function returns a n/a"

        Args:
        no arguments

        Returns:
        project_name (String)

        Raises:
        No exceptions planned"""
        if self.project_name:
            return self.project_name
        else:
            return "n/a"

    def is_reporting_allowed(self):
        """The function returns a boolean True when it is allowed to report on the project and
        on one of the reporting periods does also allow reporting

        Args:
          no arguments

        Returns:
          reporting_allowed (Boolean)

        Raises:
          No exceptions planned"""
        from koalixcrm.crm.reporting.reporting_period import ReportingPeriod
        reporting_periods = ReportingPeriod.objects.filter(project=self.id, status__is_done=False)
        if len(reporting_periods) != 0:
            if not self.project_status.is_done:
                return True
            else:
                return False
        else:
            return False

    def __str__(self):
        return str(self.id)+" "+self.get_project_name()

    class Meta:
        app_label = "crm"
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')


class ProjectAdminView(admin.ModelAdmin):
    list_display = ('id',
                    'project_status',
                    'project_name',
                    'project_manager',
                    'default_currency',
                    'planned_duration',
                    'planned_costs',
                    'effective_duration',
                    'effective_accumulated_costs'
                    )

    list_display_links = ('id',)
    ordering = ('-id',)

    fieldsets = (
        (_('Project'), {
            'fields': ('project_status',
                       'project_manager',
                       'project_name',
                       'description',
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
                                                ("/admin/crm/"+obj.__class__.__name__.lower()+"/"),
                                                obj.default_template_set.monthly_project_summary_template)
            return response

    create_report_pdf.short_description = _("Create Report PDF")


class ProjectInlineAdminView(admin.TabularInline):
    model = Project
    readonly_fields = ('link_to_project',
                       'project_status',
                       'project_manager',
                       'description',
                       'default_template_set')
    fieldsets = (
        (_('Project'), {
            'fields': ('link_to_project',
                       'project_status',
                       'project_manager',
                       'description',
                       'default_template_set')
        }),
    )
    extra = 0

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ProjectJSONSerializer(serializers.ModelSerializer):
    from koalixcrm.crm.reporting.task import TaskSerializer
    tasks = TaskSerializer(many=True, read_only=True)

    is_reporting_allowed = serializers.SerializerMethodField()

    def get_is_reporting_allowed(self, obj):
        if obj.is_reporting_allowed():
            return "True"
        else:
            return "False"

    class Meta:
        model = Project
        fields = ('id',
                  'project_manager',
                  'project_name',
                  'tasks',
                  'is_reporting_allowed')