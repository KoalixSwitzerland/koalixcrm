# -*- coding: utf-8 -*-

import factory
import datetime
from koalixcrm.crm.models import Work
from koalixcrm.crm.factories.factory_task import StandardTaskFactory
from koalixcrm.crm.factories.factory_reporting_period import StandardReportingPeriodFactory
from koalixcrm.crm.factories.factory_human_resource import StandardUserExtensionFactory
from koalixcrm.global_support_functions import make_date_utc


class StandardWorkFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Work

    human_resource = factory.SubFactory(StandardUserExtensionFactory)
    date = make_date_utc(datetime.datetime(2018, 5, 1, 0, 00))
    start_time = None
    stop_time = None
    worked_hours = "1.50"
    short_description = "The employee did some work"
    description = "And here he describes some more about his work"
    task = factory.SubFactory(StandardTaskFactory)
    reporting_period = factory.SubFactory(StandardReportingPeriodFactory)
