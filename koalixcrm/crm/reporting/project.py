# -*- coding: utf-8 -*-

from datetime import *
from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext as _
from koalixcrm.crm.reporting.genericprojectlink import InlineGenericLinks
from koalixcrm.crm.reporting.task import InlineTasks
from koalixcrm.crm.documents.pdfexport import PDFExport
from koalixcrm.crm.exceptions import TemplateSetMissingInContract


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

    def serialize_to_xml(self):
        from koalixcrm.crm.models import Task
        from koalixcrm.djangoUserExtension.models import UserExtension
        objects = [self, ]
        for task in Task.objects.filter(id=self.id):
            objects += task.objects_to_serialize()
        objects += UserExtension.objects_to_serialize(self, self.project_manager)
        main_xml = PDFExport.write_xml(objects)
        return main_xml

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
                    'project_manager',)

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

    inlines = [InlineTasks, InlineGenericLinks,]
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
                                                obj.default_template_set)
            return response

    create_report_pdf.short_description = _("Create Report PDF")


class InlineProject(admin.TabularInline):
    model = Project
    fieldsets = (
        (_('Project'), {
            'fields': ('project_status',
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
