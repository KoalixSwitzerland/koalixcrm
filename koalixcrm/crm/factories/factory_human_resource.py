# -*- coding: utf-8 -*-

import factory
from koalixcrm.crm.models import HumanResource
from koalixcrm.crm.factories.factory_user import StaffUserFactory
from koalixcrm.crm.factories.factory_resource_type import StandardResourceTypeFactory
from koalixcrm.crm.factories.factory_resource_manager import StandardResourceManagerFactory


class StandardHumanResourceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = HumanResource

    user = factory.SubFactory(StaffUserFactory)
    resource_type = factory.SubFactory(StandardResourceTypeFactory)
    resource_manager = factory.SubFactory(StandardResourceManagerFactory)
