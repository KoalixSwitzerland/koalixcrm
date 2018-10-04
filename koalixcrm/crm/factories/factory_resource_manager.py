# -*- coding: utf-8 -*-

import factory
from koalixcrm.crm.models import ResourceManager
from koalixcrm.djangoUserExtension.factories.factory_user_extension import StandardUserExtensionFactory


class StandardResourceManagerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ResourceManager

    user = factory.SubFactory(StandardUserExtensionFactory)
