# -*- coding: utf-8 -*-

import datetime

import factory

from koalixcrm.global_support_functions import make_date_utc
from koalixcrm.reporting.models.estimation import Estimation
from koalixcrm.core.tests.factories.workspace_factory import DefaultWorkspaceFactory
from koalixcrm.reporting.tests.factories.estimation_status_factory import (
    StartedEstimationStatusFactory,
)
from koalixcrm.reporting.tests.factories.human_resource_factory import (
    StandardHumanResourceFactory,
)
from koalixcrm.reporting.tests.factories.reporting_period_factory import (
    StandardReportingPeriodFactory,
)
from koalixcrm.reporting.tests.factories.resource_factory import StandardResourceFactory
from koalixcrm.reporting.tests.factories.task_factory import StandardTaskFactory


class StandardEstimationToTaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Estimation

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
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

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    amount = "112.50"
    task = factory.SubFactory(StandardTaskFactory)
    resource = factory.SubFactory(StandardHumanResourceFactory)
    date_from = make_date_utc(datetime.datetime(2018, 5, 2, 00)).date()
    date_until = make_date_utc(datetime.datetime(2018, 6, 15, 00)).date()
    status = factory.SubFactory(StartedEstimationStatusFactory)
    reporting_period = factory.SubFactory(StandardReportingPeriodFactory)
