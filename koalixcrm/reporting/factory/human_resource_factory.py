# -*- coding: utf-8 -*-

import factory
from koalixcrm.reporting.models.human_resource import HumanResource
from koalixcrm.djangoUserExtension.factories.factory_user_extension import StandardUserExtensionFactory
from koalixcrm.reporting.factory.resource_type_factory import StandardResourceTypeFactory
from koalixcrm.reporting.factory.resource_manager_factory import StandardResourceManagerFactory


class StandardHumanResourceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = HumanResource

    user = factory.SubFactory(StandardUserExtensionFactory)
    resource_type = factory.SubFactory(StandardResourceTypeFactory)
    resource_manager = factory.SubFactory(StandardResourceManagerFactory)
