# -*- coding: utf-8 -*-
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext as _
from django.contrib.contenttypes.models import ContentType
from koalixcrm.crm.exceptions import *
from koalixcrm.djangoUserExtension.exceptions import *
from koalixcrm.crm.documents.sales_document import SalesDocument
from koalixcrm.crm.documents.sales_document_position import SalesDocumentPosition
from koalixcrm.crm.reporting.task import Task
from koalixcrm.crm.reporting.generic_task_link import GenericTaskLink
from koalixcrm.crm.reporting.project import Project
from koalixcrm.global_support_functions import *
from datetime import date


class CreateTaskView:

    @staticmethod
    def create_task_from_sales_document_position(sales_document_position,
                                                 user,
                                                 document,
                                                 project):
        date_now = date.today()
        content_type_sales_document_position = ContentType.objects.get_for_model(SalesDocumentPosition)
        task_title = limit_string_length(sales_document_position.description, 30)
        try:
            existing_task = GenericTaskLink.objects.get(content_type=content_type_sales_document_position,
                                                        object_id=sales_document_position.id)
            task_id = existing_task.task.id
            task = Task.objects.filter(id=task_id).update(
                title=task_title,
                planned_start_date=date_now,
                reporting_period=project,
                description=sales_document_position.description,
                last_status_change=date_now
            )
        except ObjectDoesNotExist:
            task = Task.objects.create(
                title=task_title,
                project=project,
                description=sales_document_position.description,
                last_status_change=date_now
            )
            GenericTaskLink.objects.create(
                task=task,
                content_type=content_type_sales_document_position,
                object_id=sales_document_position.id,
                last_modified_by=user
            )
            GenericTaskLink.objects.create(
                    task=task,
                    content_type=ContentType.objects.get_for_model(SalesDocument),
                    object_id=document.id,
                    last_modified_by=user
                )
        return task

    @staticmethod
    def create_project_from_document(user, document):
        sales_document_positions = SalesDocumentPosition.objects.filter(sales_document=document)
        project_name = limit_string_length(document.contract.description, 30)
        project = Project.objects.create(project_manager=user,
                                         project_name=project_name,
                                         description=document.contract.description,
                                         default_template_set=document.contract.default_template_set,
                                         date_of_creation=date.today(),
                                         last_modification=date.today(),
                                         last_modified_by=user,
                                         default_currency=document.currency)
        for sales_document_position in sales_document_positions:
            CreateTaskView.create_task_from_sales_document_position(sales_document_position,
                                                                    user,
                                                                    document,
                                                                    project)
        return project

    @staticmethod
    def create_project(calling_model_admin, request, document, redirect_to):
        """This method creates tasks from the positions of a sales document

            Args:
              calling_model_admin (ModelAdmin):  The calling ModelAdmin must be provided for error message response.
              request: The request User is to know where to save the error message
              document (SalesDocument):  The model from which a tasks shall be created
              redirect_to (str): String that describes to where the method should redirect in case of an error

            Returns:
              HTTpResponseRedirect when not successful

            Raises:
              raises Http404 exception if anything goes wrong"""
        try:
            project = CreateTaskView.create_project_from_document(request.user, document)
            calling_model_admin.message_user(request, _("Successfully created Project and Tasks for this contract"))
            response = HttpResponseRedirect('/admin/crm/' +
                                            project.__class__.__name__.lower() +
                                            '/' +
                                            str(project.id))
        except (TemplateSetMissing,
                UserExtensionMissing,
                UserExtensionEmailAddressMissing,
                UserExtensionPhoneAddressMissing) as e:
            if isinstance(e, UserExtensionMissing):
                return render(request, 'crm/admin/exception.html')
            elif isinstance(e, UserExtensionEmailAddressMissing):
                return render(request, 'crm/admin/exception.html')
            else:
                raise Http404
        return response
