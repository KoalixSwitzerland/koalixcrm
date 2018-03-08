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
        short_description = forms.CharField(required=False)
        work_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    @staticmethod
    def generate_initial_data(start_date, stop_date):
        from koalixcrm.crm.reporting.work import Work
        list_of_work = Work.objects.filter(date__lte=stop_date).filter(date__gte=start_date)
        initial = []
        for work in list_of_work:
            initial.append({'work_id': work.id,
                            'task': work.task,
                            'projects': work.task.project,
                            'date': work.date,
                            'start_time': work.start_time,
                            'stop_time': work.stop_time,
                            'short_description': work.short_description})
        return initial

    def work_report(request):
        from koalixcrm.crm.reporting.work import Work
        monthly_report_formset = forms.formset_factory(MonthlyReportView.MonthlyReportingForm,
                                                     extra=1, max_num=60, can_delete=True)
        if request.POST.get('post'):
            formset = monthly_report_formset(request.POST)
            if 'cancel' in request.POST:
                HttpResponseRedirect('/admin/')
            elif 'register' in request.POST:
                if formset.is_valid():
                    for form in formset:
                        if form.cleaned_data['work_id']:
                            work = Work.objects.get(id=form.cleaned_data['work_id'])
                        else:
                            work = Work()
                        work.task = form.cleaned_data['task']
                        work.employee = UserExtension.get_user(request.user)
                        work.date = form.cleaned_data['date']
                        work.start_time = datetime.datetime.combine(form.cleaned_data['date'],
                                                           form.cleaned_data['start_time'])
                        work.stop_time = datetime.datetime.combine(form.cleaned_data['date'],
                                                          form.cleaned_data['stop_time'])
                        work.short_description = form.cleaned_data['short_description']
                        work.save()
                else:
                    raise InvaldidForm;
            return HttpResponseRedirect('/admin/')
        else:
            date_now = datetime.datetime.today()
            date_30days_ago = date_now-datetime.timedelta(days=30)
            initial_data = MonthlyReportView.generate_initial_data(date_30days_ago, date_now)
            formset = monthly_report_formset(initial=initial_data)
            c = {'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME, 'formset': formset}
            c.update(csrf(request))
            return render(request, 'crm/admin/time_reporting.html', c)

