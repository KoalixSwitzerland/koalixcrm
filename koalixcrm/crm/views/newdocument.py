# -*- coding: utf-8 -*-
from django.http import Http404
from django.http import HttpResponseRedirect
from django.utils.translation import gettext as _
from django.contrib import messages
from koalixcrm.crm.exceptions import *


class CreateNewDocumentView:
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
        from koalixcrm.crm.documents.contract import Contract
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
            if isinstance(calling_model, Contract):
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
