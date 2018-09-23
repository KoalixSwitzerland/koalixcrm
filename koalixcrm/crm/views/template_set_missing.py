# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.template.context_processors import csrf
from django.contrib.admin import helpers
from django.contrib.admin.widgets import *
from koalixcrm.djangoUserExtension.exceptions import TooManyUserExtensionsAvailable


class TemplateSetMissingFrom(forms.Form):
    NEXT_STEPS = (
        ('create_template_set', 'Create Required Template Set'),
        ('return_to_start', 'Return To Start'),
    )
    next_steps = forms.ChoiceField(required=True,
                                   widget=forms.Select,
                                   choices=NEXT_STEPS)


def template_set_missing(request):
    try:
        if request.POST.get('post'):
            if 'confirm_selection' in request.POST:
                user_extension_missing_form = TemplateSetMissingFrom(request.POST)
                if user_extension_missing_form.is_valid():
                    if user_extension_missing_form.cleaned_data['next_steps'] == 'return_to_start':
                        return HttpResponseRedirect('/admin/')
                    else:
                        return HttpResponseRedirect('/admin/djangoUserExtension/templatesets/')
        else:
            user_extension_missing_form = TemplateSetMissingFrom(initial={'next_steps': 'create_template_set'})
        title = "User Extension Missing"
        description = "The operation you have selected requires an existing 'Template Set' element to exist" \
                      "for the object. For one of the required objects this 'Template Set' did not exist" \
                      " Please choose one of the available options and proceed with the intended " \
                      "operation afterwards"
        c = {'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME,
             'form': user_extension_missing_form,
             'description': description,
             'title': title}
        c.update(csrf(request))
        return render(request, 'crm/admin/exception.html', c)
    except TooManyUserExtensionsAvailable:
        raise Http404


