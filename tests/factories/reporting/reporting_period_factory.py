# -*- coding: utf-8 -*-

import factory

from koalixcrm.reporting.models.reporting_period import ReportingPeriod
from tests.factories.core.workspace_factory import DefaultWorkspaceFactory
from tests.factories.reporting.project_factory import StandardProjectFactory
from tests.factories.reporting.reporting_period_status_factory import (
    ReportingReportingPeriodStatusFactory,
)


class StandardReportingPeriodFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ReportingPeriod
        django_get_or_create = ('title',)

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    project = factory.SubFactory(StandardProjectFactory)
    title = "This is a test project"
    begin = '2018-06-15'
    end = '2044-06-15'
    status = factory.SubFactory(ReportingReportingPeriodStatusFactory)
