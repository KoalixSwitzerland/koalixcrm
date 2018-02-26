# -*- coding: utf-8 -*-
from django import forms
from django.http import HttpResponseRedirect
from django.contrib.admin import helpers
from django.shortcuts import render
from django.contrib import messages
from django.template.context_processors import csrf
from django.utils.translation import ugettext as _


class MonthlyReportView:
    class MonthlyReportingForm(forms.Form):
        from koalixcrm.crm.reporting.task import Task
        from koalixcrm.crm.documents.contract import Contract
        task_list = Task.objects.all()
        tasks = forms.ModelChoiceField(task_list)
        project_list = []
        for task in task_list:
            project_list.append(task.project)
        projects = forms.ModelChoiceField(Contract.objects.all())
        date = forms.DateField()
        start_time = forms.DateTimeField()
        stop_time = forms.DateTimeField()
        short_description = forms.CharField()
        description = forms.Textarea()
        _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)

    def work_report(self, request, queryset):
        from koalixcrm.crm.reporting.work import Work
        MonthlyReportFormset = forms.formset_factory(MonthlyReportView.MonthlyReportingForm, extra=1, max_num=60)
        if request.POST.get('post'):
            formset = MonthlyReportFormset(request.POST)
            if 'cancel' in request.POST:
                self.message_user(request, _("Canceled creation of monthly report creation"), level=messages.ERROR)
                return
            elif 'register' in request.POST:
                if formset.is_valid():
                    for form in formset:
                        new_work = Work()
                        new_work.employee = request.user
                        new_work.date = form.cleaned_data['date']
                        new_work.start_time = form.cleaned_data['start_time']
                        new_work.stop_time = form.cleaned_data['stop_time']
                        new_work.short_description = form.cleaned_data['short_description']
                        new_work.description = form.cleaned_data['description']
                        new_work.save()
                        self.message_user(request, _("Successfully registered Work"))
                        return HttpResponseRedirect(request.get_full_path())
        else:
            formset = MonthlyReportFormset()
            c = {'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME, 'queryset': queryset, 'formset': formset}
            c.update(csrf(request))
            return render(request, 'crm/admin/time_reporting.html', c)

    work_report.short_description = _("Create Timesheet")