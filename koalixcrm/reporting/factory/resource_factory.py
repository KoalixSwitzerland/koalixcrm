# -*- coding: utf-8 -*-

import factory
from koalixcrm.reporting.models.resource import Resource
from koalixcrm.reporting.factory.resource_type_factory import StandardResourceTypeFactory
from koalixcrm.reporting.factory.resource_manager_factory import StandardResourceManagerFactory


class StandardResourceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Resource

    resource_type = factory.SubFactory(StandardResourceTypeFactory)
    resource_manager = factory.SubFactory(StandardResourceManagerFactory)
