# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.template.context_processors import csrf
from django.contrib.admin import helpers
from django.contrib.admin.widgets import *
from koalixcrm.djangoUserExtension.exceptions import TooManyUserExtensionsAvailable


class CreateWorkReportForm(forms.Form):
    range_from = forms.DateField(widget=AdminDateWidget)
    range_to = forms.DateField(widget=AdminDateWidget)


def create_work_report(request):
    try:
        if request.POST.get('post'):
            if 'confirm_selection' in request.POST:
                user_extension_missing_form = UserExtensionMissingForm(request.POST)
                if user_extension_missing_form.is_valid():
                    if user_extension_missing_form.cleaned_data['next_steps'] == 'return_to_start':
                        return HttpResponseRedirect('/admin/')
                    else:
                        return HttpResponseRedirect('/admin/djangoUserExtension/userextension/add/')
        else:
            user_extension_missing_form = UserExtensionMissingForm(initial={'next_steps': 'create_user_extension'})
        title = "User Extension Missing"
        description = "The operation you have selected requires an existing 'User Extension' element to exist" \
                      "for the user. For one of the required users this 'User Extension' did not exist" \
                      " Please choose one of the available options and proceed with the intended " \
                      "operation afterwards"
        c = {'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME,
             'form': user_extension_missing_form,
             'description': description,
             'title': title}
        c.update(csrf(request))
        return render(request, 'crm/admin/exception.html', c)
    except TooManyUserExtensionsAvailable as e:
        raise Http404


