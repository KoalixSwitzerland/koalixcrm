# -*- coding: utf-8 -*-
from __future__ import annotations

from datetime import date
from typing import Any

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import gettext as _

from koalixcrm.contracts.models.commercial_document import CommercialDocument
from koalixcrm.contracts.models.commercial_document_position import (
    CommercialDocumentPosition,
)
from koalixcrm.core.exceptions import *
from koalixcrm.djangoUserExtension.exceptions import *
from koalixcrm.global_support_functions import *
from koalixcrm.reporting.models.generic_task_link import GenericTaskLink
from koalixcrm.reporting.models.project import Project
from koalixcrm.reporting.models.task import Task


class CreateTaskView:

    @staticmethod
    def create_task_from_commercial_document_position(commercial_document_position: CommercialDocumentPosition,
                                                 user: Any,
                                                 document: CommercialDocument,
                                                 project: Project) -> Task:
        date_now = date.today()
        content_type_commercial_document_position = ContentType.objects.get_for_model(CommercialDocumentPosition)
        task_title = limit_string_length(commercial_document_position.description, 30)
        try:
            existing_task = GenericTaskLink.objects.get(content_type=content_type_commercial_document_position,
                                                        object_id=commercial_document_position.id)
            task_id = existing_task.task.id
            task = Task.objects.filter(id=task_id).update(
                title=task_title,
                planned_start_date=date_now,
                reporting_period=project,
                description=commercial_document_position.description,
                last_status_change=date_now
            )
        except ObjectDoesNotExist:
            task = Task.objects.create(
                title=task_title,
                project=project,
                description=commercial_document_position.description,
                last_status_change=date_now
            )
            GenericTaskLink.objects.create(
                task=task,
                content_type=content_type_commercial_document_position,
                object_id=commercial_document_position.id,
                last_modified_by=user
            )
            GenericTaskLink.objects.create(
                    task=task,
                    content_type=ContentType.objects.get_for_model(CommercialDocument),
                    object_id=document.id,
                    last_modified_by=user
                )
        return task

    @staticmethod
    def create_project_from_document(user: Any, document: CommercialDocument) -> Project:
        commercial_document_positions = CommercialDocumentPosition.objects.filter(commercial_document=document)
        project_name = limit_string_length(document.contract.description, 30)
        project = Project.objects.create(project_manager=user,
                                         project_name=project_name,
                                         description=document.contract.description,
                                         default_template_set=document.contract.default_template_set,
                                         date_of_creation=date.today(),
                                         last_modification=date.today(),
                                         last_modified_by=user,
                                         default_currency=document.currency)
        for commercial_document_position in commercial_document_positions:
            CreateTaskView.create_task_from_commercial_document_position(commercial_document_position,
                                                                    user,
                                                                    document,
                                                                    project)
        return project

    @staticmethod
    def create_project(calling_model_admin: Any, request: Any, document: CommercialDocument, redirect_to: str) -> Any:
        """This method creates tasks from the positions of a commercial document

            Args:
              calling_model_admin (ModelAdmin):  The calling ModelAdmin must be provided for error message response.
              request: The request User is to know where to save the error message
              document (CommercialDocument):  The model from which a tasks shall be created
              redirect_to (str): String that describes to where the method should redirect in case of an error

            Returns:
              HTTpResponseRedirect when not successful

            Raises:
              raises Http404 exception if anything goes wrong"""
        try:
            project = CreateTaskView.create_project_from_document(request.user, document)
            calling_model_admin.message_user(request, _("Successfully created Project and Tasks for this contract"))
            response = HttpResponseRedirect('/admin/reporting/' +
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
