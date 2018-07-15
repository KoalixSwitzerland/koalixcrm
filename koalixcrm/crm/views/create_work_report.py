# -*- coding: utf-8 -*-
import datetime
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.contrib.admin.widgets import *
from django.template.context_processors import csrf
from koalixcrm.djangoUserExtension.exceptions import TooManyUserExtensionsAvailable
from koalixcrm.crm.views.pdfexport import PDFExportView


class CreateWorkReportForm(forms.Form):
    range_from = forms.DateField(widget=AdminDateWidget)
    range_to = forms.DateField(widget=AdminDateWidget)


def create_work_report(request):
    try:
        if request.POST.get('post'):
            if 'create_pdf' in request.POST:
                create_work_report_form = CreateWorkReportForm(request.POST)
                if create_work_report_form.is_valid():
                    PDFExportView.export_pdf(calling_model_admin=None,
                                             request=request,
                                             source=user_extension,
                                             redirect_to="/admin/",
                                             template_to_use=
        else:
            datetime_now = datetime.datetime.today()
            range_from_date = (datetime_now - datetime.timedelta(days=30)).date()
            range_to_date = datetime_now.date()
            create_work_report_form = CreateWorkReportForm(initial={'range_from': range_from_date,
                                                                    'range_to': range_to_date})
        c = {'form': create_work_report_form}
        c.update(csrf(request))
        return render(request, 'crm/admin/create_work_report.html', c)
    except TooManyUserExtensionsAvailable:
        raise Http404


