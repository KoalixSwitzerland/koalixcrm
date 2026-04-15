# -*- coding: utf-8 -*-

import factory
from koalixcrm.reporting.models.resource_manager import ResourceManager
from tests.factories.djangoUserExtension.factory_user_extension import StandardUserExtensionFactory


class StandardResourceManagerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ResourceManager

    user = factory.SubFactory(StandardUserExtensionFactory)
