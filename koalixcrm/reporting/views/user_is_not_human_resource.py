# -*- coding: utf-8 -*-
from __future__ import annotations

from django.contrib.admin import helpers
from django.contrib.admin.widgets import *
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.context_processors import csrf

from koalixcrm.djangoUserExtension.exceptions import TooManyUserExtensionsAvailable


class ReportingPeriodMissingForm(forms.Form):
    NEXT_STEPS = (
        ('create_human_resource', 'Create Human Resource'),
        ('return_to_start', 'Return To Start'),
    )
    next_steps = forms.ChoiceField(required=True,
                                   widget=forms.Select,
                                   choices=NEXT_STEPS)


@login_required
def user_is_not_human_resource(request: HttpRequest) -> HttpResponse:
    try:
        if request.POST.get('post'):
            if 'confirm_selection' in request.POST:
                reporting_period_missing_form = ReportingPeriodMissingForm(request.POST)
                if reporting_period_missing_form.is_valid():
                    if reporting_period_missing_form.cleaned_data['next_steps'] == 'return_to_start':
                        return HttpResponseRedirect('/admin/')
                    else:
                        return HttpResponseRedirect('/admin/reporting/humanresource/add/')
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


