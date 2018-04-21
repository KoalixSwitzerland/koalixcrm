# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.context_processors import csrf
from django.contrib.admin.widgets import *
from koalixcrm.djangoUserExtension.models import UserExtension
from koalixcrm.crm.reporting.task import Task
from koalixcrm.crm.documents.contract import Contract
import datetime


class RangeSelectionForm(forms.Form):
    from_date = forms.DateField(widget=AdminDateWidget)
    to_date = forms.DateField(widget=AdminDateWidget)
    original_from_date = forms.DateField(widget=forms.HiddenInput(), required=False)
    original_to_date = forms.DateField(widget=forms.HiddenInput(), required=False)


class BaseWorkEntryFormset(forms.models.BaseFormSet):
    def __init__(self,*args, **kwargs):
        super(BaseWorkEntryFormset, self).__init__(*args, **kwargs)


class WorkEntry(forms.Form):
    task_list = Task.objects.all()
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
        self.original_from_date = self.from_date
        self.original_to_date = self.to_date
        project_list = []
        for task_element in self.task_list:
            project_list.append(task_element.project)
        super(WorkEntry, self).__init__(*args, **kwargs)

    def clean_date(self):
        date = self.cleaned_data['date']
        if (date < self.from_date):
            raise forms.ValidationError('date is not within the selected range', code='invalid')
        elif (self.to_date < date):
            raise forms.ValidationError('date is not within the selected range', code='invalid')
        return date

def generate_initial_data(start_date, stop_date, employee):
    from koalixcrm.crm.reporting.work import Work
    list_of_work = Work.objects.filter(employee=employee).filter(date__lte=stop_date).filter(date__gte=start_date).order_by("date")
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


def evaluate_pre_check_from_date(range_selection_form):
    original_from_date = range_selection_form.cleaned_data['original_from_date']
    new_from_date = range_selection_form.cleaned_data['from_date']
    if original_from_date < new_from_date:
        from_date = original_from_date
    else:
        from_date = new_from_date
    return from_date


def evaluate_pre_check_to_date(range_selection_form):
    original_to_date = range_selection_form.cleaned_data['original_to_date']
    new_to_date = range_selection_form.cleaned_data['to_date']

    if original_to_date > new_to_date:
        to_date = original_to_date
    else:
        to_date = new_to_date
    return to_date


def load_formset(range_selection_form, request):
    WorkEntryFormSet = forms.formset_factory(WorkEntry,
                                               extra=1,
                                               max_num=60,
                                               can_delete=True,
                                               formset=BaseWorkEntryFormset)
    from_date = evaluate_pre_check_from_date(range_selection_form)
    to_date = evaluate_pre_check_to_date(range_selection_form)
    form_kwargs = compose_form_kwargs(from_date, to_date)
    pre_check_formset = WorkEntryFormSet(request.POST,
                                         form_kwargs=form_kwargs)
    return pre_check_formset


def compose_form_kwargs(from_date, to_date):
    form_kwargs = {'from_date': from_date, 'to_date': to_date}
    return form_kwargs


def create_updated_formset(range_selection_form, request):
    WorkEntryFormSet = forms.formset_factory(WorkEntry,
                                               extra=1,
                                               max_num=60,
                                               can_delete=True,
                                               formset=BaseWorkEntryFormset)
    employee = UserExtension.get_user(request.user)
    from_date = range_selection_form.cleaned_data['from_date']
    to_date = range_selection_form.cleaned_data['to_date']
    initial_formset_data = generate_initial_data(from_date,
                                                                   to_date,
                                                                   employee)
    form_kwargs = compose_form_kwargs(from_date, to_date)
    formset = WorkEntryFormSet(initial=initial_formset_data,
                               form_kwargs=form_kwargs)
    return formset


def create_new_formset(from_date, to_date, request):
    WorkEntryFormSet = forms.formset_factory(WorkEntry,
                                               extra=1,
                                               max_num=60,
                                               can_delete=True,
                                               formset=BaseWorkEntryFormset)
    employee = UserExtension.get_user(request.user)
    initial_formset_data = generate_initial_data(from_date,
                                                                   to_date,
                                                                   employee)
    form_kwargs = compose_form_kwargs(from_date, to_date)
    formset = WorkEntryFormSet(initial=initial_formset_data,
                               form_kwargs=form_kwargs)
    return formset


def update_work(form, request):
    from koalixcrm.crm.reporting.work import Work
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


def create_range_selection_form(from_date, to_date):
    initial_form_data = {'from_date': from_date,
                         'to_date': to_date,
                         'original_from_date': from_date,
                         'original_to_date': to_date}
    range_selection_form = RangeSelectionForm(initial=initial_form_data)
    return range_selection_form


def update_range_selection_form(old_range_selection_form):
    from_date = old_range_selection_form.cleaned_data['from_date']
    to_date = old_range_selection_form.cleaned_data['to_date']
    initial_form_data = {'from_date': from_date,
                         'to_date': to_date,
                         'original_from_date': from_date,
                         'original_to_date': to_date}
    range_selection_form = RangeSelectionForm(initial=initial_form_data)
    return range_selection_form


def work_report(request):
    if request.POST.get('post'):
        if 'cancel' in request.POST:
            HttpResponseRedirect('/admin/')
        elif 'save' in request.POST:
            range_selection_form = RangeSelectionForm(request.POST)
            if range_selection_form.is_valid():
                formset = load_formset(range_selection_form,
                                                         request)
                if not formset.is_valid():
                    c = {'range_selection_form': range_selection_form,
                         'formset': formset}
                    c.update(csrf(request))
                    return render(request, 'crm/admin/time_reporting.html', c)
                else:
                    for form in formset:
                        update_work(form,request)
            formset = create_updated_formset(range_selection_form, request)
            range_selection_form = update_range_selection_form(range_selection_form)
            c = {'range_selection_form': range_selection_form,
                 'formset': formset}
            c.update(csrf(request))
            return render(request, 'crm/admin/time_reporting.html', c)
        HttpResponseRedirect('/admin/')
    else:
        datetime_now = datetime.datetime.today()
        from_date = (datetime_now - datetime.timedelta(days=30)).date()
        to_date = datetime_now.date()
        range_selection_form = create_range_selection_form(from_date, to_date)
        formset = create_new_formset(from_date, to_date, request)
        c = {'formset': formset,
             'range_selection_form': range_selection_form}
        c.update(csrf(request))
        return render(request, 'crm/admin/time_reporting.html', c)

