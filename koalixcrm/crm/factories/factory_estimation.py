# -*- coding: utf-8 -*-

import factory
import datetime
from koalixcrm.crm.models import Estimation
from koalixcrm.crm.factories.factory_resource import StandardResourceFactory
from koalixcrm.crm.factories.factory_human_resource import StandardHumanResourceFactory
from koalixcrm.crm.factories.factory_task import StandardTaskFactory
from koalixcrm.test_support_functions import make_date_utc


class StandardEstimationToTaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Estimation

    planned_effort = "112.50"
    task = factory.SubFactory(StandardTaskFactory)
    resource = factory.SubFactory(StandardResourceFactory)
    date_from = make_date_utc(datetime.datetime(2018, 5, 2, 00))
    date_to = make_date_utc(datetime.datetime(2018, 6, 15, 00))


class StandardHumanResourceEstimationToTaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Estimation

    planned_effort = "112.50"
    task = factory.SubFactory(StandardTaskFactory)
    resource = factory.SubFactory(StandardHumanResourceFactory)
    date_from = make_date_utc(datetime.datetime(2018, 5, 2, 00))
    date_to = make_date_utc(datetime.datetime(2018, 6, 15, 00))
