# -*- coding: utf-8 -*-
from os import path
from wsgiref.util import FileWrapper
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from koalixcrm.crm.exceptions import *
from koalixcrm.djangoUserExtension.exceptions import *
from django.utils.translation import gettext as _


def export_pdf(calling_model_admin, request, whereToCreateFrom, whatToCreate, redirectTo):
    """This method exports PDFs provided by different Models in the accounting application

        Args:
          calling_model_admin (ModelAdmin):  The calling ModelAdmin must be provided for error message response.
          request: The request User is required to get the Calling User TemplateSets and to know where to
          save the error message whereToCreateFrom (Model):  The model from which a PDF should be exported
          whatToCreate (str): What document Type that has to be created
          redirectTo (str): String that describes to where the method sould redirect in case of an error

        Returns:
          HTTpResponse with a PDF when successful
          HTTpResponseRedirect when not successful

        Raises:
          Http404 exception if anything goes wrong"""
    try:
        pdf = whereToCreateFrom.createPDF(request.user, whatToCreate)
        response = HttpResponse(FileWrapper(open(pdf, 'rb')), content_type='application/pdf')
        response['Content-Length'] = path.getsize(pdf)
    except (TemplateSetMissing, UserExtensionMissing) as e:
        if e.isinstance(UserExtensionMissing):
            response = HttpResponseRedirect(redirectTo)
            calling_model_admin.message_user(request, _("User Extension Missing"))
        elif e.isinstance(TemplateSetMissing):
            response = HttpResponseRedirect(redirectTo)
            calling_model_admin.message_user(request, _("Templateset Missing"))
        else:
            raise Http404
    return response


def export_xml(callingModelAdmin, request, whereToCreateFrom, whatToCreate, redirectTo):
    """This method exports XMLs provided by different Models in the accounting application

        Args:
          callingModelAdmin (ModelAdmin):  The calling ModelAdmin must be provided for error message response.
          request: The request User is required to get the Calling User TemplateSets and to know where
          to save the error message hereToCreateFrom (Model):  The model from which a PDF should be exported
          whatToCreate (str): What objects that have to be serialized
          redirectTo (str): String that describes to where the method sould redirect in case of an error

        Returns:
          HTTpResponse with a PDF when successful
          HTTpResponseRedirect when not successful

        Raises:
          raises Http404 exception if anything goes wrong"""
    try:
        xml = whereToCreateFrom.createXML(request.user, whatToCreate)
        response = HttpResponse(FileWrapper(open(xml, 'rb')), mimetype='application/xml')
        response['Content-Length'] = path.getsize(xml)
    except (TemplateSetMissing, UserExtensionMissing) as e:
        if e.isinstance(UserExtensionMissing):
            response = HttpResponseRedirect(redirectTo)
            callingModelAdmin.message_user(request, _("User Extension Missing"))
        elif e.isinstance(TemplateSetMissing):
            response = HttpResponseRedirect(redirectTo)
            callingModelAdmin.message_user(request, _("Templateset Missing"))
        else:
            raise Http404
    return response
