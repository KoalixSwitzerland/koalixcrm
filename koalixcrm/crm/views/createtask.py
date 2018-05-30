# -*- coding: utf-8 -*-
from os import path
from wsgiref.util import FileWrapper
from subprocess import CalledProcessError
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from koalixcrm.crm.exceptions import *
from koalixcrm.crm.documents.salesdocumentposition import SalesDocumentPosition


class CreateTaskView:
    def create_tasks_from_document(calling_model_admin, request, document, redirect_to):
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
            sales_document_positions = SalesDocumentPosition.objects.filter(sales_document=calling_model_admin)
            for sales_document_position in sales_document_positions:

        except (TemplateSetMissing,
                UserExtensionMissing,
                CalledProcessError,
                UserExtensionEmailAddressMissing,
                UserExtensionPhoneAddressMissing) as e:
            if isinstance(e, UserExtensionMissing):
                response = HttpResponseRedirect(redirect_to)
                calling_model_admin.message_user(request, _("User Extension Missing"))
            elif isinstance(e, UserExtensionEmailAddressMissing):
                response = HttpResponseRedirect(redirect_to)
                calling_model_admin.message_user(request, _("User Extension Email Missing"))
            else:
                raise Http404
        return response
