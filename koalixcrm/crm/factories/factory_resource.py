# -*- coding: utf-8 -*-

import factory
from koalixcrm.crm.models import Resource
from koalixcrm.crm.factories.factory_resource_type import StandardResourceTypeFactory
from koalixcrm.crm.factories.factory_resource_manager import StandardResourceManagerFactory


class StandardResourceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Resource

    resource_type = factory.SubFactory(StandardResourceTypeFactory)
    resource_manager = factory.SubFactory(StandardResourceManagerFactory)
