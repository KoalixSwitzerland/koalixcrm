# -*- coding: utf-8 -*-
from os import path
from wsgiref.util import FileWrapper
from subprocess import CalledProcessError
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from koalixcrm.crm.exceptions import *
from koalixcrm.accounting.exceptions import *


class PDFExportView:
    def export_pdf(calling_model_admin, request, document, redirect_to, template_to_use):
        """This method exports PDFs provided by different Models in the crm application

            Args:
              calling_model_admin (ModelAdmin):  The calling ModelAdmin must be provided for error message response.
              request: The request User is to know where to save the error message
              document (SalesDocument):  The model from which a PDF should be exported
              redirect_to (str): String that describes to where the method should redirect in case of an error
              template_to_use (Template Set): For some documents that need to be created there exists more
              than one template with this parameter the template set can be set during the export function


            Returns:
              HTTpResponse with a PDF when successful
              HTTpResponseRedirect when not successful

            Raises:
              raises Http404 exception if anything goes wrong"""
        try:
            pdf = document.create_pdf(template_to_use, request.user)
            response = HttpResponse(FileWrapper(open(pdf, 'rb')), content_type='application/pdf')
            response['Content-Length'] = path.getsize(pdf)
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
