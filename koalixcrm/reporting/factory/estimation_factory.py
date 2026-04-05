# -*- coding: utf-8 -*-

import factory
import datetime
from koalixcrm.reporting.models.estimation import Estimation
from koalixcrm.reporting.factory.resource_factory import StandardResourceFactory
from koalixcrm.reporting.factory.human_resource_factory import StandardHumanResourceFactory
from koalixcrm.reporting.factory.reporting_period_factory import StandardReportingPeriodFactory
from koalixcrm.reporting.factory.estimation_status_factory import StartedEstimationStatusFactory
from koalixcrm.reporting.factory.task_factory import StandardTaskFactory
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
