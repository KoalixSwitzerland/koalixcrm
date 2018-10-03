# -*- coding: utf-8 -*-

import factory
from koalixcrm.crm.models import ResourceManager
from koalixcrm.crm.factories.factory_user import StaffUserFactory


class StandardResourceManagerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ResourceManager

    user = factory.SubFactory(StaffUserFactory)
