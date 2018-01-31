# -*- coding: utf-8 -*-
from os import path
from wsgiref.util import FileWrapper
from django.contrib import messages
from subprocess import CalledProcessError

from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from koalixcrm.crm.exceptions import *
from rest_framework import viewsets
from koalixcrm.crm.documents.salesdocumentposition import SalesDocumentPosition, SalesContractPositionJSONSerializer


def export_pdf(calling_model_admin, request, document, redirect_to):
    """This method exports PDFs provided by different Models in the crm application

        Args:
          calling_model_admin (ModelAdmin):  The calling ModelAdmin must be provided for error message response.
          request: The request User is to know where to save the error message
          document (Contract):  The model from which a PDF should be exported
          redirect_to (str): String that describes to where the method should redirect in case of an error

        Returns:
          HTTpResponse with a PDF when successful
          HTTpResponseRedirect when not successful

        Raises:
          raises Http404 exception if anything goes wrong"""
    try:
        pdf = document.create_pdf()
        response = HttpResponse(FileWrapper(open(pdf, 'rb')), content_type='application/pdf')
        response['Content-Length'] = path.getsize(pdf)
    except (TemplateSetMissing, UserExtensionMissing, CalledProcessError, UserExtensionEmailAddressMissing, UserExtensionPhoneAddressMissing) as e:
        if isinstance(e, UserExtensionMissing):
            response = HttpResponseRedirect(redirect_to)
            calling_model_admin.message_user(request, _("User Extension Missing"))
        elif isinstance(e, UserExtensionEmailAddressMissing):
            response = HttpResponseRedirect(redirect_to)
            calling_model_admin.message_user(request, _("User Extension Email Missing"))
        elif isinstance(e, UserExtensionPhoneAddressMissing):
            response = HttpResponseRedirect(redirect_to)
            calling_model_admin.message_user(request, _("User Extension Phone Missing"))
        elif isinstance(e, TemplateSetMissing):
            response = HttpResponseRedirect(redirect_to)
            calling_model_admin.message_user(request, _("Templateset Missing"))
        elif isinstance(e, TemplateFOPConfigFileMissing):
            response = HttpResponseRedirect(redirect_to)
            calling_model_admin.message_user(request, _("Fop Config File Missing in TemplateSet"))
        elif isinstance(e, TemplateXSLTFileMissing):
            response = HttpResponseRedirect(redirect_to)
            calling_model_admin.message_user(request, _("XSLT File Missing in TemplateSet"))
        elif type(e) == CalledProcessError:
            response = HttpResponseRedirect(redirect_to)
            calling_model_admin.message_user(request, e.output)
        else:
            raise Http404
    return response


def create_new_document(calling_model_admin, request, calling_model, requested_document_type, redirect_to):
    """This method exports PDFs provided by different Models in the crm application

        Args:
          calling_model_admin (ModelAdmin):  The calling ModelAdmin must be provided for error message response.
          request: The request User is to know where to save the error message
          calling_model (Contract or SalesDocument):  The model from which a new document shall be created
          requested_document_type (str): The document type name that shall be created
          redirect_to (str): String that describes to where the method should redirect in case of an error

        Returns:
          HTTpResponse with a PDF when successful
          HTTpResponseRedirect when not successful

        Raises:
          raises Http404 exception if anything goes wrong"""
    try:
        new_document = requested_document_type()
        new_document.create_from_reference(calling_model)
        calling_model_admin.message_user(request, _(str(new_document) +
                                                    " created"))
        response = HttpResponseRedirect('/admin/crm/'+
                                        new_document.__class__.__name__.lower()+
                                        '/'+
                                        str(new_document.id))
    except (TemplateSetMissingInContract, TemplateMissingInTemplateSet) as e:
        if isinstance(calling_model, koalixcrm.crm.documents.contract.Contract):
            contract = calling_model
        else:
            contract = calling_model.contract
        if isinstance(e, TemplateSetMissingInContract):
            response = HttpResponseRedirect('/admin/crm/contract/'+
                                            str(contract.id))
            calling_model_admin.message_user(request, _("Missing Templateset "),
                                             level=messages.ERROR)
        elif isinstance(e, TemplateMissingInTemplateSet):
            response = HttpResponseRedirect('/admin/djangoUserExtension/templateset/' +
                                            str(contract.default_template_set.id))
            calling_model_admin.message_user(request,
                                             (_("Missing template for ")+
                                              new_document.__class__.__name__),
                                             level=messages.ERROR)
        else:
            raise Http404
    return response


class SalesContractPositionAsJSON(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed.
    """
    queryset = SalesDocumentPosition.objects.all()
    serializer_class = SalesContractPositionJSONSerializer
