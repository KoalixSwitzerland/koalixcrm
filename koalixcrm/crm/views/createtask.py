# -*- coding: utf-8 -*-
from django.http import Http404
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext as _
from koalixcrm.crm.exceptions import *
from koalixcrm.crm.documents.salesdocument import SalesDocument
from koalixcrm.crm.documents.salesdocumentposition import SalesDocumentPosition
from koalixcrm.crm.reporting.task import Task
from koalixcrm.crm.reporting.generictasklink import GenericTaskLink
from django.contrib.contenttypes.models import ContentType
from datetime import date


class CreateTaskView:

    def create_task_from_sales_document_position(sales_document_position, request, document):
        date_now = date.today()
        contract = document.contract
        content_type_sales_document_position = ContentType.objects.get_for_model(SalesDocumentPosition)
        try:
            existing_task = GenericTaskLink.objects.get(content_type=content_type_sales_document_position,
                                                    object_id=sales_document_position.id)
            task_id = existing_task.task.id
            task = Task.objects.filter(id=task_id).update(
                short_description=sales_document_position.description[:30] +
                                  (sales_document_position.description[30:] and '..'),
                planned_start_date=date_now,
                project=contract,
                description=sales_document_position.description,
                last_status_change=date_now
            )
        except ObjectDoesNotExist:
            task = Task.objects.create(
                short_description=sales_document_position.description[:30] +
                                  (sales_document_position.description[30:] and '..'),
                planned_start_date=date_now,
                project=contract,
                description=sales_document_position.description,
                last_status_change=date_now
            )
            GenericTaskLink.objects.create(
                task=task,
                content_type=content_type_sales_document_position,
                object_id=sales_document_position.id,
                last_modified_by=request.user
            )
            GenericTaskLink.objects.create(
                    task=task,
                    content_type=ContentType.objects.get_for_model(SalesDocument),
                    object_id=document.id,
                    last_modified_by=request.user
                )
        return task

    def create_tasks_from_document(calling_model_admin, request, document, redirect_to):
        """This method creates tasks from the positions of a sales document

            Args:
              calling_model_admin (ModelAdmin):  The calling ModelAdmin must be provided for error message response.
              request: The request User is to know where to save the error message
              document (SalesDocument):  The model from which a tasks shall be created
              redirect_to (str): String that describes to where the method should redirect in case of an error

            Returns:
              HTTpResponse with a PDF when successful
              HTTpResponseRedirect when not successful

            Raises:
              raises Http404 exception if anything goes wrong"""
        try:
            sales_document_positions = SalesDocumentPosition.objects.filter(sales_document=document)
            for sales_document_position in sales_document_positions:
                CreateTaskView.create_task_from_sales_document_position(sales_document_position,
                                                                        request,
                                                                        document)
            calling_model_admin.message_user(request, _("Successfully created Tasks for this contract"))
            response = HttpResponseRedirect(redirect_to)
        except (TemplateSetMissing,
                UserExtensionMissing,
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
