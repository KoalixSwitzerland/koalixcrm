# -*- coding: utf-8 -*-
from django import forms
from django.http import HttpResponseRedirect
from django.contrib.admin import helpers
from django.shortcuts import render
from django.template.context_processors import csrf
from django.contrib.admin.widgets import *
from koalixcrm.djangoUserExtension.models import UserExtension
import datetime


class MonthlyReportView:

    class RangeSelectionForm(forms.Form):
        from_date = forms.DateField(widget=AdminDateWidget)
        to_date = forms.DateField(widget=AdminDateWidget)

    class BaseWorkEntryFormset(forms.models.BaseFormSet):
        def __init__(self,*args, **kwargs):
            super(MonthlyReportView.BaseWorkEntryFormset, self).__init__(*args, **kwargs)

    class WorkEntry(forms.Form):

        from koalixcrm.crm.reporting.task import Task
        from koalixcrm.crm.documents.contract import Contract
        task_list = Task.objects.all()
        project_list = []
        for task_element in task_list:
            project_list.append(task_element.project)
        projects = forms.ModelChoiceField(Contract.objects.all())
        task = forms.ModelChoiceField(task_list)
        date = forms.DateField(widget=AdminDateWidget)
        start_time = forms.TimeField(widget=AdminTimeWidget)
        stop_time = forms.TimeField(widget=AdminTimeWidget)
        short_description = forms.CharField(required=False)
        work_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)

        def __init__(self, *args, **kwargs ):
            self.from_date = kwargs.pop('from_date')
            self.to_date = kwargs.pop('to_date')
            super(MonthlyReportView.WorkEntry, self).__init__(*args, **kwargs)

        def cleanby(self):
            cleaned_data = super(MonthlyReportView.WorkEntry, self).clean()
            if (cleaned_data['date'] < self.from_date):
                raise forms.ValidationError('You have selected a date which is not within the define limits')
            elif (self.to_date < cleaned_data['date']):
                raise forms.ValidationError('You have selected a date which is not within the define limits')
            return cleaned_data

    @staticmethod
    def generate_initial_data(start_date, stop_date):
        from koalixcrm.crm.reporting.work import Work
        list_of_work = Work.objects.filter(date__lte=stop_date).filter(date__gte=start_date).order_by("date")
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
        WorkEntryFormSet = forms.formset_factory(MonthlyReportView.WorkEntry,
                                                   extra=1,
                                                   max_num=60,
                                                   can_delete=True,
                                                   formset=MonthlyReportView.BaseWorkEntryFormset)
        if request.POST.get('post'):
            formset = WorkEntryFormSet(request.POST,
                                       form_kwargs={'from_date': datetime.date.today(),
                                                    'to_date': datetime.date.today()})
            range_selection_form = MonthlyReportView.RangeSelectionForm(request.POST)
            if 'cancel' in request.POST:
                HttpResponseRedirect('/admin/')
            elif 'save' in request.POST:
                if range_selection_form.is_valid():
                    if formset.is_valid():
                        for form in formset:
                            if form.has_changed():
                                if form.cleaned_data['work_id']:
                                    work = Work.objects.get(id=form.cleaned_data['work_id'])
                                else:
                                    work = Work()
                                if form.cleaned_data['DELETE']:
                                    work.delete()
                                else:
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
                    c = {'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME,
                         'range_selection_form': range_selection_form,
                         'formset': formset}
                    c.update(csrf(request))
                    return render(request, 'crm/admin/time_reporting.html', c)
            return HttpResponseRedirect('/koalixcrm/crm/reporting/monthlyreport/')
        else:
            date_now = datetime.datetime.today()
            date_30days_ago = date_now-datetime.timedelta(days=30)
            initial_formset_data = MonthlyReportView.generate_initial_data(date_30days_ago, date_now)
            formset = WorkEntryFormSet(initial=initial_formset_data,
                                       form_kwargs={'from_date': datetime.date.today(),
                                                    'to_date': datetime.date.today()})
            initial_form_data = {'from_date': date_30days_ago, 'to_date': date_now}
            range_selection_form = MonthlyReportView.RangeSelectionForm(initial=initial_form_data)
            c = {'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME,
                 'formset': formset,
                 'range_selection_form': range_selection_form}
            c.update(csrf(request))
            return render(request, 'crm/admin/time_reporting.html', c)

