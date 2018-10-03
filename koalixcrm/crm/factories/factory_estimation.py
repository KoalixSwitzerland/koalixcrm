# -*- coding: utf-8 -*-

import factory
from koalixcrm.crm.models import Estimation
from koalixcrm.crm.factories.factory_resource import StandardResourceFactory
from koalixcrm.crm.factories.factory_human_resource import StandardHumanResourceFactory
from koalixcrm.crm.factories.factory_task import StandardTaskFactory


class StandardEstimationToTaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Estimation

    planned_effort = "112.50"
    task = factory.SubFactory(StandardTaskFactory)
    resource = factory.SubFactory(StandardResourceFactory)


class StandardHumanResourceEstimationToTaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Estimation

    planned_effort = "112.50"
    task = factory.SubFactory(StandardTaskFactory)
    resource = factory.SubFactory(StandardHumanResourceFactory)