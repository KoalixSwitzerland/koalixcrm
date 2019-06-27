# -*- coding: utf-8 -*-

import factory
from koalixcrm.crm.models import ReportingPeriod
from koalixcrm.crm.factories.factory_project import StandardProjectFactory
from koalixcrm.crm.factories.factory_reporting_period_status import ReportingReportingPeriodStatusFactory


class StandardReportingPeriodFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ReportingPeriod
        django_get_or_create = ('title',)

    project = factory.SubFactory(StandardProjectFactory)
    title = "This is a test project"
    begin = '2018-06-15'
    end = '2044-06-15'
    status = factory.SubFactory(ReportingReportingPeriodStatusFactory)
