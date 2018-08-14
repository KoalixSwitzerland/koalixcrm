# -*- coding: utf-8 -*-

import factory
from koalixcrm.crm.models import Task
from koalixcrm.crm.factories.factory_project import StandardProjectFactory
from koalixcrm.crm.factories.factory_task_status import StartedTaskStatusFactory


class StandardTaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task

    title = 'This is a test Task'
    planned_start_date = '2018-05-02'
    planned_end_date = '2018-06-15'
    project = factory.SubFactory(StandardProjectFactory)
    description = "This is a description"
    status = factory.SubFactory(StartedTaskStatusFactory)
    last_status_change = '2018-06-15'
