# -*- coding: utf-8 -*-

import factory
from django.contrib.contenttypes.models import ContentType

from koalixcrm.reporting.models.generic_task_link import GenericTaskLink
from tests.factories.contacts.user_factory import StaffUserFactory
from tests.factories.core.workspace_factory import DefaultWorkspaceFactory
from tests.factories.reporting.project_factory import StandardProjectFactory
from tests.factories.reporting.task_factory import StandardTaskFactory
from tests.factories.reporting.task_link_type_factory import (
    RelatedToTaskLinkTypeFactory,
)


class StandardGenericTaskLinkFactory(factory.django.DjangoModelFactory):
    class Meta:
        exclude = ['generic_crm_object']

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    task = factory.SubFactory(StandardTaskFactory)
    task_link_type = factory.SubFactory(RelatedToTaskLinkTypeFactory)
    content_type = factory.LazyAttribute(
        lambda o: ContentType.objects.get_for_model(o.generic_crm_object))
    object_id = factory.SelfAttribute('generic_crm_object.id')
    date_of_creation = "2018-05-01"
    last_modified_by = factory.SubFactory(StaffUserFactory)


class LinkToProjectGenericTaskLinkFactory(StandardGenericTaskLinkFactory):
    class Meta:
        model = GenericTaskLink

    generic_crm_object = factory.SubFactory(StandardProjectFactory)
