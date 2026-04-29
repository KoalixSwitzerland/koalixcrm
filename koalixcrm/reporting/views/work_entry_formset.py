# -*- coding: utf-8 -*-
from __future__ import annotations

import datetime
from typing import Any

from django import forms

from koalixcrm.reporting.views.work_entry_form import WorkEntry


class BaseWorkEntryFormset(forms.BaseFormSet):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(BaseWorkEntryFormset, self).__init__(*args, **kwargs)

    @staticmethod
    def generate_initial_data(start_date: datetime.date, stop_date: datetime.date, human_resource: Any) -> list[dict[str, Any]]:
        from koalixcrm.reporting.models.work import Work

        list_of_work = Work.objects.filter(
            human_resource=human_resource, date__lte=stop_date, date__gte=start_date
        ).order_by("date")
        initial = []
        for work in list_of_work:
            initial.append(
                {
                    "work_id": work.id,
                    "task": work.task,
                    "project": work.task.project,
                    "datetime_start": work.start_time,
                    "datetime_stop": work.stop_time,
                    "worked_hours": work.worked_hours,
                    "description": work.description,
                }
            )
        return initial

    @staticmethod
    def load_formset(range_selection_form: Any, request: Any) -> Any:
        WorkEntryFormSet = forms.formset_factory(
            WorkEntry, extra=1, max_num=60, can_delete=True, formset=BaseWorkEntryFormset
        )
        from_date = range_selection_form.evaluate_pre_check_from_date()
        to_date = range_selection_form.evaluate_pre_check_to_date()
        form_kwargs = BaseWorkEntryFormset.compose_form_kwargs(from_date, to_date)
        pre_check_formset = WorkEntryFormSet(request.POST, form_kwargs=form_kwargs)
        return pre_check_formset

    @staticmethod
    def compose_form_kwargs(from_date: datetime.date, to_date: datetime.date) -> dict[str, Any]:
        form_kwargs = {"from_date": from_date, "to_date": to_date}
        return form_kwargs

    @staticmethod
    def create_updated_formset(range_selection_form: Any, human_resource: Any) -> Any:
        WorkEntryFormSet = forms.formset_factory(
            WorkEntry, extra=1, max_num=60, can_delete=True, formset=BaseWorkEntryFormset
        )
        from_date = range_selection_form.cleaned_data["from_date"]
        to_date = range_selection_form.cleaned_data["to_date"]
        initial_formset_data = BaseWorkEntryFormset.generate_initial_data(from_date, to_date, human_resource)
        form_kwargs = BaseWorkEntryFormset.compose_form_kwargs(from_date, to_date)
        formset = WorkEntryFormSet(initial=initial_formset_data, form_kwargs=form_kwargs)
        return formset

    @staticmethod
    def create_new_formset(from_date: datetime.date, to_date: datetime.date, human_resource: Any) -> Any:
        WorkEntryFormSet = forms.formset_factory(
            WorkEntry, extra=1, max_num=60, can_delete=True, formset=BaseWorkEntryFormset
        )
        initial_formset_data = BaseWorkEntryFormset.generate_initial_data(from_date, to_date, human_resource)
        form_kwargs = BaseWorkEntryFormset.compose_form_kwargs(from_date, to_date)
        formset = WorkEntryFormSet(initial=initial_formset_data, form_kwargs=form_kwargs)
        return formset
