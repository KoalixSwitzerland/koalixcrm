# -*- coding: utf-8 -*-
from os import path
from subprocess import *
from wsgiref.util import FileWrapper

from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from koalixcrm.crm.exceptions import TemplateSetMissing
from koalixcrm.crm.exceptions import UserExtensionMissing
from koalixcrm.crm.models import *


def exportPDF(callingModelAdmin, request, whereToCreateFrom, whatToCreate, redirectTo):
    """This method exports PDFs provided by different Models in the crm application

        Args:
          callingModelAdmin (ModelAdmin):  The calling ModelAdmin must be provided for error message response.
          request: The request User is to know where to save the error message
          whereToCreateFrom (Model):  The model from which a PDF should be exported
          whatToCreate (str): What document Type that has to be
          redirectTo (str): String that describes to where the method sould redirect in case of an error

        Returns:
              HTTpResponse with a PDF when successful
              HTTpResponseRedirect when not successful

        Raises:
          raises Http404 exception if anything goes wrong"""
    try:
        pdf = whereToCreateFrom.createPDF(whatToCreate)
        response = HttpResponse(FileWrapper(open(pdf, 'rb')), content_type='application/pdf')
        response['Content-Length'] = path.getsize(pdf)
    except (TemplateSetMissing, UserExtensionMissing, CalledProcessError) as e:
        if type(e) == UserExtensionMissing:
            response = HttpResponseRedirect(redirectTo)
            callingModelAdmin.message_user(request, _("User Extension Missing"))
        elif type(e) == TemplateSetMissing:
            response = HttpResponseRedirect(redirectTo)
            callingModelAdmin.message_user(request, _("Templateset Missing"))
        elif type(e) == CalledProcessError:
            response = HttpResponseRedirect(redirectTo)
            callingModelAdmin.message_user(request, e.output)
        else:
            raise Http404
    return response


def selectaddress(invoiceid):
    invoice = Invoice.objects.get(id=invoiceid)
    address = invoice.contract
