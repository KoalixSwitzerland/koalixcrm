# -*- coding: utf-8 -*-
from django import forms
from django.http import HttpResponseRedirect
from django.contrib.admin import helpers
from django.shortcuts import render
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

    @staticmethod
    def generate_initial_data(start_date, stop_date):
        from koalixcrm.crm.reporting.work import Work
        list_of_work = Work.objects.filter(date__lte=stop_date).filter(date__gte=start_date)
        initial = []
        for work in list_of_work:
            initial.append({'task': work.task,
                            'projects': work.task.project,
                            'date': work.date,
                            'start_time': work.start_time,
                            'stop_time': work.stop_time,
                            'short_description': work.short_description})
        return initial

    def work_report(request):
        from koalixcrm.crm.reporting.work import Work
        MonthlyReportFormset = forms.formset_factory(MonthlyReportView.MonthlyReportingForm, extra=5, max_num=60, can_delete=True)
        if request.POST.get('post'):
            formset = MonthlyReportFormset(request.POST)
            if 'cancel' in request.POST:
                HttpResponseRedirect('/admin/')
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
            return HttpResponseRedirect('/admin/')
        else:
            formset = MonthlyReportFormset(initial=MonthlyReportView.generate_initial_data(datetime.datetime.today()-datetime.timedelta(days=30),
                                                                                   datetime.datetime.today()))
            c = {'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME, 'formset': formset}
            c.update(csrf(request))
            return render(request, 'crm/admin/time_reporting.html', c)

