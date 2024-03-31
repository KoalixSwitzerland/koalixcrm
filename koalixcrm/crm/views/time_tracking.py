# -*- coding: utf-8 -*-

import datetime
from django.http import HttpResponseRedirect, Http404
from django.contrib import messages
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
from koalixcrm.djangoUserExtension.models import UserExtension
from koalixcrm.crm.exceptions import ReportingPeriodNotFound
from koalixcrm.crm.exceptions import UserIsNoHumanResource
from koalixcrm.djangoUserExtension.exceptions import UserExtensionMissing, TooManyUserExtensionsAvailable
from koalixcrm.crm.views.range_selection_form import RangeSelectionForm
from koalixcrm.crm.views.work_entry_formset import BaseWorkEntryFormset
from koalixcrm.crm.reporting.human_resource import HumanResource


@login_required
def work_report(request):
    try:
        human_resource = HumanResource.objects.filter(user=UserExtension.get_user_extension(request.user))
        if len(human_resource) == 0:
            error_message = "User "+request.user.__str__()+" is not registered as human resource"
            raise UserIsNoHumanResource(error_message)
        else:
            human_resource = HumanResource.objects.get(user=UserExtension.get_user_extension(request.user))
        if request.POST.get('post'):
            if 'cancel' in request.POST:
                return HttpResponseRedirect('/admin/')
            elif 'save' in request.POST:
                range_selection_form = RangeSelectionForm(request.POST)
                if range_selection_form.is_valid():
                    formset = BaseWorkEntryFormset.load_formset(range_selection_form,
                                                                request)
                    if not formset.is_valid():
                        c = {'range_selection_form': range_selection_form,
                             'formset': formset}
                        c.update(csrf(request))
                        return render(request, 'crm/admin/time_reporting.html', c)
                    else:
                        for form in formset:
                            form.update_work(request)
                        messages.success(request, _('you have successfully updated your work'))
                formset = BaseWorkEntryFormset.create_updated_formset(range_selection_form,
                                                                      human_resource)
                range_selection_form.update_from_input()
                c = {'range_selection_form': range_selection_form,
                     'formset': formset}
                c.update(csrf(request))
                return render(request, 'crm/admin/time_reporting.html', c)
            return HttpResponseRedirect('/admin/')
        else:
            datetime_now = datetime.datetime.today()
            to_date = (datetime_now + datetime.timedelta(days=30)).date()
            from_date = datetime_now.date()
            range_selection_form = RangeSelectionForm.create_range_selection_form(from_date, to_date)
            formset = BaseWorkEntryFormset.create_new_formset(from_date,
                                                              to_date,
                                                              human_resource)
            c = {'formset': formset,
                 'range_selection_form': range_selection_form}
            c.update(csrf(request))
            return render(request, 'crm/admin/time_reporting.html', c)
    except (UserExtensionMissing,
            ReportingPeriodNotFound,
            TooManyUserExtensionsAvailable,
            UserIsNoHumanResource) as e:
        if isinstance(e, UserExtensionMissing):
            return HttpResponseRedirect(e.view)
        elif isinstance(e, ReportingPeriodNotFound):
            return HttpResponseRedirect(e.view)
        elif isinstance(e, TooManyUserExtensionsAvailable):
            return HttpResponseRedirect(e.view)
        elif isinstance(e, UserIsNoHumanResource):
            return HttpResponseRedirect(e.view)
        else:
            raise Http404
