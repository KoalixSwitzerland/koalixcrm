# -*- coding: utf-8 -*-

import datetime
from dateutil.relativedelta import *
from django.db import models
from django.contrib import admin
from django.utils.translation import gettext as _
from koalixcrm.djangoUserExtension.user_extension.user_extension import UserExtension
from koalixcrm.crm.reporting.resource import Resource
from koalixcrm.crm.reporting.resource_price import ResourcePriceInlineAdminView
from koalixcrm.crm.reporting.work import Work
from koalixcrm.crm.documents.pdf_export import PDFExport


class HumanResource(Resource):
    user = models.ForeignKey(UserExtension,
                             on_delete=models.CASCADE,
                             verbose_name=_("User"))

    def __str__(self):
        return self.user.__str__()

    def serialize_to_xml(self, **kwargs):
        date_from = kwargs.get('date_from', datetime.date.today()-datetime.timedelta(days=60))
        date_to = kwargs.get('date_to', datetime.date.today())
        date_first_of_the_month = date_from.replace(day=1)
        date_first_of_next_month = date_from.replace(day=1) + relativedelta(months=+1)
        date_end_of_the_month = date_first_of_next_month - datetime.timedelta(days=1)
        date = date_first_of_the_month
        days = dict()
        weeks = dict()
        months = dict()
        projects = self.resource_contribution_project(date_from, date_to)
        objects = [self, self.user]
        objects.extend(projects)
        main_xml = PDFExport.write_xml(objects)
        while date < date_from:
            project_efforts = dict()
            for project in projects:
                project_efforts[project] = {'effort': "-",
                                            'project': project.id.__str__()}
            days[date] = {'effort': "-",
                          "day": str(date.day),
                          "week": str(date.isocalendar()[1]),
                          "week_day": str(date.isoweekday()),
                          "month": str(date.month),
                          "year": str(date.year),
                          "project_efforts": project_efforts}
            date += datetime.timedelta(days=1)
        while date <= date_to:
            project_efforts_day = dict()
            project_efforts_week = dict()
            project_efforts_month = dict()
            for project in projects:
                project_efforts_day[project] = {'effort': 0,
                                                'project': project.id.__str__()}
                project_efforts_week[project] = {'effort': 0,
                                                 'project': project.id.__str__()}
                project_efforts_month[project] = {'effort': 0,
                                                  'project': project.id.__str__()}
            days[date] = {'effort': 0,
                          "day": str(date.day),
                          "week": str(date.isocalendar()[1]),
                          "week_day": str(date.isoweekday()),
                          "month": str(date.month),
                          "year": str(date.year),
                          "project_efforts": project_efforts_day}
            month_key = str(date.month)+"/"+str(date.year)
            week_key = str(date.isocalendar()[1])+"/"+str(date.year)
            if not (week_key in weeks):
                weeks[week_key] = {'effort': 0,
                                   'week': str(date.isocalendar()[1]),
                                   'year': str(date.year),
                                   "project_efforts": project_efforts_week}
            if not (month_key in months):
                months[month_key] = {'effort': 0,
                                     'month': str(date.month),
                                     'year': str(date.year),
                                     "project_efforts": project_efforts_month}
            date += datetime.timedelta(days=1)
        while date < date_end_of_the_month:
            project_efforts = dict()
            for project in projects:
                project_efforts[project] = {'effort': "-",
                                            'project': project.id.__str__()}
            days[date] = {'effort': "-",
                          "day": str(date.day),
                          "week": str(date.isocalendar()[1]),
                          "week_day": str(date.isoweekday()),
                          "month": str(date.month),
                          "year": str(date.year),
                          "project_efforts": project_efforts}
            date += datetime.timedelta(days=1)
        main_xml = PDFExport.append_element_to_pattern(main_xml,
                                                       ".",
                                                       "range_from",
                                                       date_from.__str__(),
                                                       attributes={"day": str(date_from.day),
                                                                   "week": str(date_from.isocalendar()[1]),
                                                                   "week_day": str(date_from.isoweekday()),
                                                                   "month": str(date_from.month),
                                                                   "year": str(date_from.year)})
        main_xml = PDFExport.append_element_to_pattern(main_xml,
                                                       ".",
                                                       "range_to",
                                                       date_to.__str__(),
                                                       attributes={"day": str(date_to.day),
                                                                   "week": str(date_to.isocalendar()[1]),
                                                                   "week_day": str(date_to.isoweekday()),
                                                                   "month": str(date_to.month),
                                                                   "year": str(date_to.year)})
        works = Work.objects.filter(human_resource=self, date__range=(date_from, date_to))
        for work in works:
            days[work.date]['effort'] += work.effort_hours()
            days[work.date]['project_efforts'][work.task.project]['effort'] += work.effort_hours()
            month_key = str(work.date.month)+"/"+str(work.date.year)
            week_key = str(work.date.isocalendar()[1])+"/"+str(work.date.year)
            weeks[week_key]['effort'] += work.effort_hours()
            weeks[week_key]['project_efforts'][work.task.project]['effort'] += work.effort_hours()
            months[month_key]['effort'] += work.effort_hours()
            months[month_key]['project_efforts'][work.task.project]['effort'] += work.effort_hours()
            work_xml = work.serialize_to_xml()
            main_xml = PDFExport.merge_xml(main_xml, work_xml)
        for day_key in days.keys():
            main_xml = PDFExport.append_element_to_pattern(main_xml,
                                                           "object/[@model='djangoUserExtension.userextension']",
                                                           "Day_Work_Hours",
                                                           str(days[day_key]['effort']),
                                                           attributes={"day": days[day_key]['day'],
                                                                       "week": days[day_key]['week'],
                                                                       "week_day": days[day_key]['week_day'],
                                                                       "month": days[day_key]['month'],
                                                                       "year": days[day_key]['year']})
            for project_key in days[day_key]['project_efforts'].keys():
                main_xml = PDFExport.append_element_to_pattern(main_xml,
                                                               "object/[@model='djangoUserExtension.userextension']",
                                                               "Day_Project_Work_Hours",
                                                               str(days[day_key]['project_efforts'][project_key]['effort']),
                                                               attributes={"day": days[day_key]['day'],
                                                                           "week": days[day_key]['week'],
                                                                           "week_day": days[day_key]['week_day'],
                                                                           "month": days[day_key]['month'],
                                                                           "year": days[day_key]['year'],
                                                                           "project": days[day_key]['project_efforts'][project_key]['project']})
        for week_key in weeks.keys():
            main_xml = PDFExport.append_element_to_pattern(main_xml,
                                                           "object/[@model='djangoUserExtension.userextension']",
                                                           "Week_Work_Hours",
                                                           str(weeks[week_key]['effort']),
                                                           attributes={"week": weeks[week_key]['week'],
                                                                       "year": weeks[week_key]['year']})
            for project_key in weeks[week_key]['project_efforts'].keys():
                main_xml = PDFExport.append_element_to_pattern(main_xml,
                                                               "object/[@model='djangoUserExtension.userextension']",
                                                               "Week_Project_Work_Hours",
                                                               str(weeks[week_key]['project_efforts'][project_key]['effort']),
                                                               attributes={"week": weeks[week_key]['week'],
                                                                           "year": weeks[week_key]['year'],
                                                                           "project": weeks[week_key]['project_efforts'][project_key]['project']})
        for month_key in months.keys():
            main_xml = PDFExport.append_element_to_pattern(main_xml,
                                                           "object/[@model='djangoUserExtension.userextension']",
                                                           "Month_Work_Hours",
                                                           str(months[month_key]['effort']),
                                                           attributes={"month": months[month_key]['month'],
                                                                       "year": months[month_key]['year']})
            for project_key in months[month_key]['project_efforts'].keys():
                main_xml = PDFExport.append_element_to_pattern(main_xml,
                                                               "object/[@model='djangoUserExtension.userextension']",
                                                               "Month_Project_Work_Hours",
                                                               str(months[month_key]['project_efforts'][project_key]['effort']),
                                                               attributes={"month": months[month_key]['month'],
                                                                           "year": months[month_key]['year'],
                                                                           "project": months[month_key]['project_efforts'][project_key]['project']})
        return main_xml

    def create_pdf(self, template_set, printed_by, *args, **kwargs):
        return PDFExport.create_pdf(self, template_set, printed_by, *args, **kwargs)

    def get_template_set(self, template_set):
        return self.user.get_template_set(template_set)

    def get_fop_config_file(self, template_set):
        return self.user.get_fop_config_file(template_set)

    def get_xsl_file(self, template_set):
        return self.user.get_xsl_file(template_set)

    def resource_contribution_project(self, date_from, date_to):
        works = Work.objects.filter(human_resource=self,
                                    date__range=(date_from, date_to))
        projects = []
        for work in works:
            if work.task.project not in projects:
                projects.append(work.task.project)
        return projects


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
