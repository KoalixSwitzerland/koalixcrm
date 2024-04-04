# -*- coding: utf-8 -*-

from django import forms
from koalixcrm.crm.views.work_entry_form import WorkEntry


class BaseWorkEntryFormset(forms.BaseFormSet):
    def __init__(self, *args, **kwargs):
        super(BaseWorkEntryFormset, self).__init__(*args, **kwargs)

    @staticmethod
    def generate_initial_data(start_date, stop_date, human_resource):
        from koalixcrm.crm.reporting.work import Work
        list_of_work = Work.objects.filter(human_resource=human_resource, date__lte=stop_date, date__gte=start_date).order_by("date")
        initial = []
        for work in list_of_work:
            initial.append({'work_id': work.id,
                            'task': work.task,
                            'project': work.task.project,
                            'datetime_start': work.start_time,
                            'datetime_stop': work.stop_time,
                            'worked_hours': work.worked_hours,
                            'description': work.description})
        return initial

    @staticmethod
    def load_formset(range_selection_form, request):
        WorkEntryFormSet = forms.formset_factory(WorkEntry,
                                                 extra=1,
                                                 max_num=60,
                                                 can_delete=True,
                                                 formset=BaseWorkEntryFormset)
        from_date = range_selection_form.evaluate_pre_check_from_date()
        to_date = range_selection_form.evaluate_pre_check_to_date()
        form_kwargs = BaseWorkEntryFormset.compose_form_kwargs(from_date, to_date)
        pre_check_formset = WorkEntryFormSet(request.POST,
                                             form_kwargs=form_kwargs)
        return pre_check_formset

    @staticmethod
    def compose_form_kwargs(from_date, to_date):
        form_kwargs = {'from_date': from_date, 'to_date': to_date}
        return form_kwargs

    @staticmethod
    def create_updated_formset(range_selection_form, human_resource):
        WorkEntryFormSet = forms.formset_factory(WorkEntry,
                                                 extra=1,
                                                 max_num=60,
                                                 can_delete=True,
                                                 formset=BaseWorkEntryFormset)
        from_date = range_selection_form.cleaned_data['from_date']
        to_date = range_selection_form.cleaned_data['to_date']
        initial_formset_data = BaseWorkEntryFormset.generate_initial_data(from_date,
                                                                          to_date,
                                                                          human_resource)
        form_kwargs = BaseWorkEntryFormset.compose_form_kwargs(from_date, to_date)
        formset = WorkEntryFormSet(initial=initial_formset_data,
                                   form_kwargs=form_kwargs)
        return formset

    @staticmethod
    def create_new_formset(from_date, to_date, human_resource):
        WorkEntryFormSet = forms.formset_factory(WorkEntry,
                                                 extra=1,
                                                 max_num=60,
                                                 can_delete=True,
                                                 formset=BaseWorkEntryFormset)
        initial_formset_data = BaseWorkEntryFormset.generate_initial_data(from_date,
                                                                          to_date,
                                                                          human_resource)
        form_kwargs = BaseWorkEntryFormset.compose_form_kwargs(from_date,
                                                               to_date)
        formset = WorkEntryFormSet(initial=initial_formset_data,
                                   form_kwargs=form_kwargs)
        return formset
