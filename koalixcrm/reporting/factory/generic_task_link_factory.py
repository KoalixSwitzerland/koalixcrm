# -*- coding: utf-8 -*-

import factory
from koalixcrm.reporting.models.generic_task_link import GenericTaskLink
from koalixcrm.reporting.factory.task_factory import StandardTaskFactory
from koalixcrm.reporting.factory.task_link_type_factory import RelatedToTaskLinkTypeFactory
from koalixcrm.crm.factory.user_factory import StaffUserFactory
from koalixcrm.reporting.factory.project_factory import StandardProjectFactory
from django.contrib.contenttypes.models import ContentType


class StandardGenericTaskLinkFactory(factory.django.DjangoModelFactory):
    class Meta:
        exclude = ['generic_crm_object']

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
