# -*- coding: utf-8 -*-
from django import forms
from django.http import HttpResponseRedirect
from django.contrib.admin import helpers
from django.shortcuts import render
from django.contrib import messages
from django.template.context_processors import csrf
from django.utils.translation import ugettext as _
from django.contrib.admin.widgets import *
from koalixcrm.djangoUserExtension.models import UserExtension
import datetime


class MonthlyReportView:

    class MonthlyReportingForm(forms.Form):
        from koalixcrm.crm.reporting.task import Task
        from koalixcrm.crm.documents.contract import Contract
        task_list = Task.objects.all()
        task = forms.ModelChoiceField(task_list)
        project_list = []
        for task_element in task_list:
            project_list.append(task_element.project)
        projects = forms.ModelChoiceField(Contract.objects.all())
        date = forms.DateField(widget=AdminDateWidget)
        start_time = forms.TimeField(widget=AdminTimeWidget)
        stop_time = forms.TimeField(widget=AdminTimeWidget)
        short_description = forms.CharField()

    def work_report(self, calling_admin, request, queryset):
        from koalixcrm.crm.reporting.work import Work
        MonthlyReportFormset = forms.formset_factory(MonthlyReportView.MonthlyReportingForm, extra=1, max_num=60)
        if request.POST.get('post'):
            formset = MonthlyReportFormset(request.POST)
            if 'cancel' in request.POST:
                calling_admin.message_user(request, _("Canceled creation of monthly report creation"), level=messages.ERROR)
                return
            elif 'register' in request.POST:
                if formset.is_valid():
                    for form in formset:
                        new_work = Work()
                        new_work.task = form.cleaned_data['task']
                        new_work.employee = UserExtension.get_user(request.user)
                        new_work.date = form.cleaned_data['date']
                        new_work.start_time = datetime.datetime.combine(form.cleaned_data['date'],
                                                               form.cleaned_data['start_time'])
                        new_work.stop_time = datetime.datetime.combine(form.cleaned_data['date'],
                                                              form.cleaned_data['stop_time'])
                        new_work.short_description = form.cleaned_data['short_description']
                        new_work.save()
                    calling_admin.message_user(request, _("Successfully registered Work"))
                else:
                    calling_admin.message_user(request, _("Not Successfully registered Work"))
            return HttpResponseRedirect(request.get_full_path())
        else:
            formset = forms.formset_factory(MonthlyReportView.MonthlyReportingForm, extra=1, max_num=60)
            c = {'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME, 'queryset': queryset, 'formset': formset}
            c.update(csrf(request))
            return render(request, 'crm/admin/time_reporting.html', c)

    work_report.short_description = _("Create Timesheet")



