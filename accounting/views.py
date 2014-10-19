# -*- coding: utf-8 -*-
from os import path

from django.core.servers.basehttp import FileWrapper
from django.http import Http404
from django.http import HttpResponse


def export_pdf(calling_model_admin, request, where_to_create_form, what_to_create, redirect_to):
    """This method exports PDFs provided by different Models in the accounting application

        Args:
          calling_model_admin (ModelAdmin):  The calling ModelAdmin must be provided for error message response.
          request: The request User is required to get the Calling User TemplateSets and to know where to save the
                    error message
          where_to_create_form (Model):  The model from which a PDF should be exported
          what_to_create (str): What document Type that has to be
          redirect_to (str): String that describes to where the method sould redirect in case of an error

        Returns:
              HTTpResponse with a PDF when successful
              HTTpResponseRedirect when not successful

        Raises:
          raises Http404 exception if anything goes wrong"""
    try:
        pdf = where_to_create_form.create_pdf(request.user, what_to_create)
        response = HttpResponse(FileWrapper(file(pdf)), mimetype='application/pdf')
        response['Content-Length'] = path.getsize(pdf)
    # except (TemplateSetMissing, UserExtensionMissing, CalledProcessError), e:
    # if type(e) == UserExtensionMissing:
    #         response = HttpResponseRedirect(redirect_to)
    #         calling_model_admin.message_user(request, _("User Extension Missing"))
    #     elif type(e) == TemplateSetMissing:
    #         response = HttpResponseRedirect(redirect_to)
    #         calling_model_admin.message_user(request, _("Templateset Missing"))
    #     elif type(e) == CalledProcessError:
    #         response = HttpResponseRedirect(redirect_to)
    #         calling_model_admin.message_user(request, e.output)
    #     else:
    #         raise Http404
    except Exception, err:
        raise Http404
    return response
