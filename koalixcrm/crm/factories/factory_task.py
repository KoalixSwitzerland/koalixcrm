# -*- coding: utf-8 -*-

import factory
from koalixcrm.crm.models import Task
from koalixcrm.crm.factories.factory_project import StandardProjectFactory


class StandardTaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task

    title = 'This is a test Task'
    planned_start_date = '2018-05-02'
    planned_end_date = '2018-06-15'
    project = factory.SubFactory(StandardProjectFactory)
    description = factory.Faker('description')
    status = factory.Faker('status')
    last_status_change = factory.Faker('last_status_change')
