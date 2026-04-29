# -*- coding: utf-8 -*-

import datetime

import factory

from koalixcrm.global_support_functions import make_date_utc
from koalixcrm.reporting.models.estimation import Estimation
from tests.factories.core.workspace_factory import DefaultWorkspaceFactory
from tests.factories.reporting.estimation_status_factory import (
    StartedEstimationStatusFactory,
)
from tests.factories.reporting.human_resource_factory import (
    StandardHumanResourceFactory,
)
from tests.factories.reporting.reporting_period_factory import (
    StandardReportingPeriodFactory,
)
from tests.factories.reporting.resource_factory import StandardResourceFactory
from tests.factories.reporting.task_factory import StandardTaskFactory


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
