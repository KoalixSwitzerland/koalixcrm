# -*- coding: utf-8 -*-

import factory
from koalixcrm.crm.models import ResourceType


class StandardResourceTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ResourceType

    title = 'This is a test Resource Type'
    description = "This is a description of such a Resource Type"
