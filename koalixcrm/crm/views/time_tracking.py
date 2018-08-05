# -*- coding: utf-8 -*-
import datetime
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.template.context_processors import csrf
from django.contrib.admin.widgets import *
from django.forms import NumberInput
from django.contrib.auth.decorators import login_required
from koalixcrm.djangoUserExtension.models import UserExtension
from koalixcrm.crm.reporting.task import Task
from koalixcrm.crm.reporting.project import Project
from koalixcrm.crm.reporting.reporting_period import ReportingPeriod
from koalixcrm.crm.exceptions import ReportingPeriodNotFound
from koalixcrm.djangoUserExtension.exceptions import UserExtensionMissing, TooManyUserExtensionsAvailable
from koalixcrm.globalSupportFunctions import limit_string_length


class RangeSelectionForm(forms.Form):
    from_date = forms.DateField(widget=AdminDateWidget)
    to_date = forms.DateField(widget=AdminDateWidget)
    original_from_date = forms.DateField(widget=forms.HiddenInput(), required=False)
    original_to_date = forms.DateField(widget=forms.HiddenInput(), required=False)


class BaseWorkEntryFormset(forms.models.BaseFormSet):
    def __init__(self,*args, **kwargs):
        super(BaseWorkEntryFormset, self).__init__(*args, **kwargs)


class WorkEntry(forms.Form):
    project = forms.ModelChoiceField(queryset=Project.objects.filter(reportingperiod__status__is_done=False),
                                     required=True)
    task = forms.ModelChoiceField(queryset=Task.objects.filter(status__is_done=False),
                                  required=True)
    date = forms.DateField(widget=AdminDateWidget, required=True)
    start_time = forms.TimeField(widget=AdminTimeWidget, required=False)
    stop_time = forms.TimeField(widget=AdminTimeWidget, required=False)
    worked_hours = forms.DecimalField(widget=NumberInput(attrs={'step': 0.1,
                                                                'min': 0,
                                                                'max': 24}),
                                      required=False)
    description = forms.CharField(widget=AdminTextareaWidget, required=True)
    work_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        self.from_date = kwargs.pop('from_date')
        self.to_date = kwargs.pop('to_date')
        self.original_from_date = self.from_date
        self.original_to_date = self.to_date
        super(WorkEntry, self).__init__(*args, **kwargs)

    @staticmethod
    def check_working_hours(cleaned_data):
        """This method checks that the working hour is correctly proved either using the start_stop pattern
        or by providing the worked_hours in total.

        Args:
          cleaned_data (Dict):  The cleaned_data must contain the values form the form validation.
          The django built in form validation must already have been passed

        Returns:
          True when no ValidationError was raised

        Raises:
          may raise ValidationError exception"""
        start_stop_pattern_complete = ("start_time" in cleaned_data) & ("stop_time" in cleaned_data)
        start_stop_pattern_stop_missing = ("start_time" in cleaned_data) & ("stop_time" not in cleaned_data)
        start_stop_pattern_start_missing = ("stop_time" in cleaned_data) & ("start_time" not in cleaned_data)
        worked_hours_pattern = "worked_hours" in cleaned_data
        if start_stop_pattern_complete & worked_hours_pattern:
            raise forms.ValidationError('Please either set the start, stop time or worked hours (not both)',
                                        code='invalid')
        elif start_stop_pattern_start_missing or start_stop_pattern_stop_missing:
            raise forms.ValidationError('Set start and stop time',
                                        code='invalid')
        return True

    def clean(self):
        cleaned_data = super(WorkEntry, self).clean()
        date = cleaned_data['date']
        if date < self.from_date:
            raise forms.ValidationError('date is not within the selected range', code='invalid')
        elif self.to_date < date:
            raise forms.ValidationError('date is not within the selected range', code='invalid')
        elif not cleaned_data["project"].is_reporting_allowed():
            raise forms.ValidationError('The project is either closed or there is not '
                                        'reporting period available', code='invalid')
        return cleaned_data


def generate_initial_data(start_date, stop_date, employee):
    from koalixcrm.crm.reporting.work import Work
    list_of_work = Work.objects.filter(employee=employee).filter(date__lte=stop_date).filter(date__gte=start_date).order_by("date")
    initial = []
    for work in list_of_work:
        initial.append({'work_id': work.id,
                        'task': work.task,
                        'project': work.task.project,
                        'date': work.date,
                        'start_time': work.start_time,
                        'stop_time': work.stop_time,
                        'worked_hours': work.worked_hours,
                        'description': work.description})
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
    employee = UserExtension.get_user_extension(request.user)
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
    employee = UserExtension.get_user_extension(request.user)
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
            work.reporting_period = ReportingPeriod.get_reporting_period(project=form.cleaned_data['task'].project,
                                                                         search_date=form.cleaned_data['date'])
        if form.cleaned_data['DELETE']:
            work.delete()
        else:
            work.task = form.cleaned_data['task']
            work.employee = UserExtension.get_user_extension(request.user)
            work.date = form.cleaned_data['date']
            work.start_time = datetime.datetime.combine(form.cleaned_data['date'],
                                                        form.cleaned_data['start_time'])
            work.stop_time = datetime.datetime.combine(form.cleaned_data['date'],
                                                       form.cleaned_data['stop_time'])
            work.worked_hours = form.cleaned_data['worked_hours']
            work.description = form.cleaned_data['description']
            work.short_description = limit_string_length(work.description, 100)
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


@login_required
def work_report(request):
    try:
        if request.POST.get('post'):
            if 'cancel' in request.POST:
                return HttpResponseRedirect('/admin/')
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
            return HttpResponseRedirect('/admin/')
        else:
            datetime_now = datetime.datetime.today()
            to_date = (datetime_now + datetime.timedelta(days=30)).date()
            from_date = datetime_now.date()
            range_selection_form = create_range_selection_form(from_date, to_date)
            formset = create_new_formset(from_date, to_date, request)
            c = {'formset': formset,
                 'range_selection_form': range_selection_form}
            c.update(csrf(request))
            return render(request, 'crm/admin/time_reporting.html', c)
    except (UserExtensionMissing,
            ReportingPeriodNotFound,
            TooManyUserExtensionsAvailable) as e:
        if isinstance(e, UserExtensionMissing):
            return HttpResponseRedirect(e.view)
        elif isinstance(e, ReportingPeriodNotFound):
            return HttpResponseRedirect(e.view)
        elif isinstance(e, TooManyUserExtensionsAvailable):
            return HttpResponseRedirect(e.view)
        elif isinstance(e, UserExtensionPhoneAddressMissing):
            return HttpResponseRedirect(e.view)
        else:
            raise Http404
