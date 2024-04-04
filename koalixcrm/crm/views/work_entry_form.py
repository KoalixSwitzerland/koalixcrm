# -*- coding: utf-8 -*-

from django.forms import NumberInput
from koalixcrm.crm.reporting.task import Task
from koalixcrm.crm.reporting.project import Project
from django.contrib.admin.widgets import *
from koalixcrm.global_support_functions import limit_string_length
from koalixcrm.djangoUserExtension.models import UserExtension
from koalixcrm.crm.reporting.reporting_period import ReportingPeriod
from koalixcrm.crm.reporting.human_resource import HumanResource


class WorkEntry(forms.Form):
    """
    Form which allows to fill out a full Work. Instead of only showing the task, it is possible
    to select the task based on the input from the project
    """
    project = forms.ModelChoiceField(queryset=Project.objects.filter(reportingperiod__status__is_done=False).distinct(),
                                     required=True)
    task = forms.ModelChoiceField(queryset=Task.objects.filter(status__is_done=False),
                                  required=True)
    datetime_start = forms.SplitDateTimeField(widget=AdminSplitDateTime,
                                              required=True)
    datetime_stop = forms.SplitDateTimeField(widget=AdminSplitDateTime,
                                             required=False)
    worked_hours = forms.DecimalField(widget=NumberInput(attrs={'step': 0.1,
                                                                'min': 0,
                                                                'max': 24}),
                                      required=False)
    description = forms.CharField(widget=AdminTextareaWidget,
                                  required=True)
    work_id = forms.IntegerField(widget=forms.HiddenInput(),
                                 required=False)

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
        if ("datetime_start" in cleaned_data) & ("datetime_stop" in cleaned_data) & ("worked_hours" in cleaned_data):
            start_stop_pattern_complete = bool(cleaned_data["datetime_start"]) & bool(cleaned_data["datetime_stop"])
            start_stop_pattern_stop_missing = bool(cleaned_data["datetime_start"]) & (not bool(cleaned_data["datetime_stop"]))
            start_stop_pattern_start_missing = (not bool(cleaned_data["datetime_start"])) & bool(cleaned_data["datetime_stop"])
            worked_hours_pattern = bool(cleaned_data["worked_hours"])
        else:
            raise forms.ValidationError('Programming error', code='invalid')
        if start_stop_pattern_complete & worked_hours_pattern:
            raise forms.ValidationError('Please either set the start, stop time or worked hours (not both)',
                                        code='invalid')
        elif start_stop_pattern_start_missing or start_stop_pattern_stop_missing:
            raise forms.ValidationError('Set start and stop time',
                                        code='invalid')
        elif not start_stop_pattern_complete and not worked_hours_pattern:
            raise forms.ValidationError('Either fill out the start_time and stop_time or the worked_hours',
                                        code='invalid')
        return True

    def clean(self):
        cleaned_data = super(WorkEntry, self).clean()
        if 'date' in cleaned_data:
            date = cleaned_data['date']
            if date < self.from_date:
                raise forms.ValidationError('date is not within the selected range', code='invalid')
            elif self.to_date < date:
                raise forms.ValidationError('date is not within the selected range', code='invalid')
        if 'project' in cleaned_data:
            if not cleaned_data["project"].is_reporting_allowed():
                raise forms.ValidationError('The project is either closed or there is not '
                                            'reporting period available', code='invalid')
        WorkEntry.check_working_hours(cleaned_data)
        return cleaned_data

    def update_work(self, request):
        from koalixcrm.crm.reporting.work import Work
        if self.has_changed():
            if self.cleaned_data['work_id']:
                work = Work.objects.get(id=self.cleaned_data['work_id'])
            else:
                if not self.cleaned_data['DELETE']:
                    work = Work()
                else:
                    return
            if self.cleaned_data['DELETE']:
                work.delete()
            else:
                work.task = self.cleaned_data['task']
                work.reporting_period = ReportingPeriod.get_reporting_period(project=self.cleaned_data['task'].project,
                                                                             search_date=self.cleaned_data['datetime_start'].date())
                work.human_resource = HumanResource.objects.get(user=UserExtension.get_user_extension(request.user))
                work.date = self.cleaned_data['datetime_start'].date()
                if bool(self.cleaned_data['datetime_start']) & bool(self.cleaned_data['datetime_stop']):
                    work.start_time = self.cleaned_data['datetime_start']
                    work.stop_time = self.cleaned_data['datetime_stop']
                else:
                    work.worked_hours = self.cleaned_data['worked_hours']
                work.description = self.cleaned_data['description']
                work.short_description = limit_string_length(work.description, 100)
                work.save()
