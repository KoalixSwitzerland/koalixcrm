# -*- coding: utf-8 -*-

import factory
from koalixcrm.crm.models import ReportingPeriod
from koalixcrm.crm.factories.factory_project import StandardProjectFactory
from koalixcrm.crm.factories.factory_reporting_period_status import ReportingReportingPeriodStatusFactory


class StandardReportingPeriodFactory(factory.Factory):
    class Meta:
        model = ReportingPeriod

    project = factory.SubFactory(StandardProjectFactory)
    title = "This is a test project"
    begin = '2018-06-15'
    end = '2019-06-15'
    status = factory.SubFactory(ReportingReportingPeriodStatusFactory)
