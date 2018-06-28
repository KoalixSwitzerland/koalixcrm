# -*- coding: utf-8 -*-

from datetime import *
from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext as _
from django.utils.html import format_html
from koalixcrm.crm.reporting.genericprojectlink import InlineGenericLinks
from koalixcrm.crm.reporting.task import InlineTasks
from koalixcrm.crm.documents.pdfexport import PDFExport
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
                                                       self.effective_effort(reporting_period=None))
        if reporting_period:
            main_xml = PDFExport.append_element_to_pattern(main_xml,
                                                           "object/[@model='crm.project']",
                                                           "Effective_Effort_InPeriod",
                                                           self.effective_effort(reporting_period=reporting_period))
        main_xml = PDFExport.append_element_to_pattern(main_xml,
                                                       "object/[@model='crm.project']",
                                                       "Planned_Effort",
                                                       self.planned_effort())
        main_xml = PDFExport.append_element_to_pattern(main_xml,
                                                       "object/[@model='crm.project']",
                                                       "Effective_Duration",
                                                       self.effective_duration())
        main_xml = PDFExport.append_element_to_pattern(main_xml,
                                                       "object/[@model='crm.project']",
                                                       "Planned_Duration",
                                                       self.planned_duration())
        return main_xml

    def effective_effort_overall(self):
        return self.effective_effort(reporting_period=None)

    def effective_effort(self, reporting_period):
        effective_effort_accumulated = 0
        for task in Task.objects.filter(project=self.id):
            effective_effort_accumulated += task.effective_effort(reporting_period=reporting_period)
        return effective_effort_accumulated

    def planned_effort(self):
        planned_effort_accumulated = 0
        for task in Task.objects.filter(project=self.id):
            planned_effort_accumulated += task.planned_effort()
        return planned_effort_accumulated

    def effective_duration(self):
        return "n/a"

    def planned_start(self):
        tasks = Task.objects.filter(project=self.id)
        if tasks:
            i = 0
            for task in tasks:
                if i == 0:
                    project_start = task.planned_start_date
                elif task.planned_start_date < project_start:
                    project_start = task.planned_start_date
                i = i+1
            return project_start
        else:
            None

    def planned_end(self):
        i = 0
        for task in Task.objects.filter(project=self.id):
            if i == 0:
                project_start = task.planned_start_date
            elif task.planned_start_date < project_start:
                project_start = task.planned_start_date
            i = i+1
        else:
            None

    def planned_duration(self):
        if (not self.planned_start()) or (not self.planned_end()):
            return 0
        elif self.planned_start() > self.planned_end():
            return 0
        else:
            return self.planned_end()-self.planned_start()

    def get_project_name(self):
        if self.project_name:
            return self.project_name
        else:
            return "n/a"

    def __str__(self):
        return str(self.id)+" "+self.get_project_name()

    class Meta:
        app_label = "crm"
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')


class OptionProject(admin.ModelAdmin):
    list_display = ('id',
                    'project_status',
                    'project_name',
                    'project_manager',
                    'planned_effort',
                    'effective_effort_overall',
                    'planned_duration',
                    'effective_duration')

    list_display_links = ('id',)
    ordering = ('-id',)

    fieldsets = (
        (_('Project'), {
            'fields': ('project_status',
                       'project_manager',
                       'project_name',
                       'description',
                       'default_template_set')
        }),
    )

    inlines = [InlineTasks, InlineGenericLinks]
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


class InlineProject(admin.TabularInline):
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


class ProjectJSONSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = ('id',
                  'project_manager',
                  'project_name')