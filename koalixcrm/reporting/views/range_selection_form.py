# -*- coding: utf-8 -*-

from django.contrib.admin.widgets import *


class RangeSelectionForm(forms.Form):
    """
    Form which allows to select the Range in which the work item can be registered
    and which define which range of work items are loaded from the database and shown
    to the user
    """
    from_date = forms.DateField(widget=AdminDateWidget)
    to_date = forms.DateField(widget=AdminDateWidget)
    original_from_date = forms.DateField(widget=forms.HiddenInput(),
                                         required=False)
    original_to_date = forms.DateField(widget=forms.HiddenInput(),
                                       required=False)

    def evaluate_pre_check_from_date(self):
        original_from_date = self.cleaned_data['original_from_date']
        new_from_date = self.cleaned_data['from_date']
        if original_from_date < new_from_date:
            from_date = original_from_date
        else:
            from_date = new_from_date
        return from_date

    def evaluate_pre_check_to_date(self):
        original_to_date = self.cleaned_data['original_to_date']
        new_to_date = self.cleaned_data['to_date']

        if original_to_date > new_to_date:
            to_date = original_to_date
        else:
            to_date = new_to_date
        return to_date

    def update_from_input(self):
        self.from_date = self.cleaned_data['from_date']
        self.to_date = self.cleaned_data['to_date']
        self.original_from_date = self.from_date
        self.original_to_date = self.to_date

    @staticmethod
    def create_range_selection_form(from_date, to_date):
        initial_form_data = {'from_date': from_date,
                             'to_date': to_date,
                             'original_from_date': from_date,
                             'original_to_date': to_date}
        range_selection_form = RangeSelectionForm(initial=initial_form_data)
        return range_selection_form

