# -*- coding: utf-8 -*-

import factory
from koalixcrm.reporting.models.generic_project_link import GenericProjectLink
from tests.factories.reporting.project_factory import StandardProjectFactory
from tests.factories.reporting.task_link_type_factory import RelatedToTaskLinkTypeFactory
from tests.factories.crm.user_factory import StaffUserFactory
from tests.factories.reporting.task_factory import StandardTaskFactory
from django.contrib.contenttypes.models import ContentType


class StandardGenericTaskLinkFactory(factory.django.DjangoModelFactory):
    class Meta:
        exclude = ['generic_crm_object']

    task = factory.SubFactory(StandardProjectFactory)
    task_link_type = factory.SubFactory(RelatedToTaskLinkTypeFactory)
    content_type = factory.LazyAttribute(
        lambda o: ContentType.objects.get_for_model(o.generic_crm_object))
    object_id = factory.SelfAttribute('generic_crm_object.id')
    date_of_creation = "2018-05-01"
    last_modified_by = factory.SubFactory(StaffUserFactory)


class LinkToTaskGenericTaskLinkFactory(StandardGenericTaskLinkFactory):
    class Meta:
        model = GenericProjectLink

    generic_crm_object = factory.SubFactory(StandardTaskFactory)
