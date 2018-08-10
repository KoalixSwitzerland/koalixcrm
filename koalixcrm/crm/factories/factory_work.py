# -*- coding: utf-8 -*-

import factory
from koalixcrm.crm.models import Work
from koalixcrm.crm.factories.factory_user import StaffUserFactory
from koalixcrm.crm.factories.factory_task import StandardTaskFactory
from koalixcrm.crm.factories.factory_reporting_period import StandardReportingPeriodFactory


class StandardWorkFactory(factory.Factory):
    class Meta:
        model = Work

    employee = factory.SubFactory(StaffUserFactory)
    date = "2018-05-01"
    start_time = None
    stop_time = None
    worked_hours = "1.50"
    short_description = "The employee did some work"
    description = "And here he describes some more about his work"
    task = factory.SubFactory(StandardTaskFactory)
    reporting_period = factory.SubFactory(StandardReportingPeriodFactory)
