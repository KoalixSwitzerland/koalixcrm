# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.template.context_processors import csrf
from django.contrib.admin import helpers
from django.contrib.admin.widgets import *
from koalixcrm.djangoUserExtension.exceptions import TooManyUserExtensionsAvailable


class ReportingPeriodMissingForm(forms.Form):
    NEXT_STEPS = (
        ('create_human_resource', 'Create Human Resource'),
        ('return_to_start', 'Return To Start'),
    )
    next_steps = forms.ChoiceField(required=True,
                                   widget=forms.Select,
                                   choices=NEXT_STEPS)


def user_is_not_human_resource(request):
    try:
        if request.POST.get('post'):
            if 'confirm_selection' in request.POST:
                reporting_period_missing_form = ReportingPeriodMissingForm(request.POST)
                if reporting_period_missing_form.is_valid():
                    if reporting_period_missing_form.cleaned_data['next_steps'] == 'return_to_start':
                        return HttpResponseRedirect('/admin/')
                    else:
                        return HttpResponseRedirect('/admin/crm/humanresource/add/')
        else:
            reporting_period_missing_form = ReportingPeriodMissingForm(initial={'next_steps': 'create_user_extension'})
        title = "User is not registered as Human Resource"
        description = "The operation you have selected requires that the currently active user is a registered " \
                      "as a Human Resource. "
        c = {'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME,
             'form': reporting_period_missing_form,
             'description': description,
             'title': title}
        c.update(csrf(request))
        return render(request, 'crm/admin/exception.html', c)
    except TooManyUserExtensionsAvailable:
        raise Http404


