# -*- coding: utf-8 -*-

import factory
import datetime
from koalixcrm.crm.models import Estimation
from koalixcrm.crm.factories.factory_resource import StandardResourceFactory
from koalixcrm.crm.factories.factory_human_resource import StandardHumanResourceFactory
from koalixcrm.crm.factories.factory_reporting_period import StandardReportingPeriodFactory
from koalixcrm.crm.factories.factory_estimation_status import StartedEstimationStatusFactory
from koalixcrm.crm.factories.factory_task import StandardTaskFactory
from koalixcrm.global_support_functions import make_date_utc


class StandardEstimationToTaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Estimation

    amount = "112.50"
    task = factory.SubFactory(StandardTaskFactory)
    resource = factory.SubFactory(StandardResourceFactory)
    date_from = make_date_utc(datetime.datetime(2018, 5, 2, 00)).date()
    date_until = make_date_utc(datetime.datetime(2018, 6, 15, 00)).date()
    status = factory.SubFactory(StartedEstimationStatusFactory)
    reporting_period = factory.SubFactory(StandardReportingPeriodFactory)


class StandardHumanResourceEstimationToTaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Estimation

    amount = "112.50"
    task = factory.SubFactory(StandardTaskFactory)
    resource = factory.SubFactory(StandardHumanResourceFactory)
    date_from = make_date_utc(datetime.datetime(2018, 5, 2, 00)).date()
    date_until = make_date_utc(datetime.datetime(2018, 6, 15, 00)).date()
    status = factory.SubFactory(StartedEstimationStatusFactory)
    reporting_period = factory.SubFactory(StandardReportingPeriodFactory)
