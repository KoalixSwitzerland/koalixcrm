# -*- coding: utf-8 -*-

import factory
from koalixcrm.crm.models import HumanResource
from koalixcrm.crm.factories.factory_user import StaffUserFactory


class StandardHumanResourceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = HumanResource

    user = factory.SubFactory(StaffUserFactory)
