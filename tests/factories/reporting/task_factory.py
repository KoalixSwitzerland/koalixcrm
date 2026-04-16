# -*- coding: utf-8 -*-

import factory
import datetime
from koalixcrm.reporting.models.task import Task
from tests.factories.reporting.project_factory import StandardProjectFactory
from tests.factories.reporting.task_status_factory import StartedTaskStatusFactory
from koalixcrm.global_support_functions import make_date_utc


class StandardTaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task

    title = 'This is a test Task'
    project = factory.SubFactory(StandardProjectFactory)
    description = "This is a description"
    status = factory.SubFactory(StartedTaskStatusFactory)
    last_status_change = make_date_utc(datetime.datetime(2018, 6, 15, 00))
