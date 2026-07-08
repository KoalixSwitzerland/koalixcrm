# -*- coding: utf-8 -*-

import datetime

import factory

from koalixcrm.global_support_functions import make_date_utc
from koalixcrm.reporting.models.task import Task
from koalixcrm.core.tests.factories.workspace_factory import DefaultWorkspaceFactory
from koalixcrm.reporting.tests.factories.project_factory import StandardProjectFactory
from koalixcrm.reporting.tests.factories.task_status_factory import StartedTaskStatusFactory


class StandardTaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    title = 'This is a test Task'
    project = factory.SubFactory(StandardProjectFactory)
    description = "This is a description"
    status = factory.SubFactory(StartedTaskStatusFactory)
    last_status_change = make_date_utc(datetime.datetime(2018, 6, 15, 00))
