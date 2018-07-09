# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.context_processors import csrf
from django.contrib.admin import helpers
from django.contrib.admin.widgets import *
from django.contrib.auth.decorators import login_required
from koalixcrm.djangoUserExtension.models import UserExtension
from koalixcrm.crm.reporting.task import Task
from koalixcrm.crm.reporting.project import Project
from koalixcrm.crm.reporting.reporting_period import ReportingPeriod
from koalixcrm.crm.exceptions import ReportingPeriodNotFound
from koalixcrm.djangoUserExtension.exceptions import UserExtensionMissing, TooManyUserExtensionsAvailable

import datetime
from koalixcrm.globalSupportFunctions import limit_string_length

class UserExtensionMissingForm(forms.Form):
    NEXT_STEPS = (
        ('create_user_extension', 'Create User Extension'),
        ('return_to_start', 'Return To Start'),
    )
    next_steps = forms.ChoiceField(required=True,
                                   widget=forms.Select,
                                   choices=NEXT_STEPS)
@login_required
def user_extension_missing(request):
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
            form = UserExtensionMissingForm(initial={'next_steps': 'return_to_start'})
            title = "User Extension Missing"
            description = "Choose next steps"
            c = {'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME,
                 'form': form,
                 'description': description,
                 'title': title}
            c.update(csrf(request))
            return render(request, 'crm/admin/exception.html', c)
    except (TooManyUserExtensionsAvailable) as e:
        raise Http404


