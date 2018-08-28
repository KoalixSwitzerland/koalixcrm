# -*- coding: utf-8 -*-

import factory
from koalixcrm.crm.models import TaskStatus


class DoneTaskStatusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TaskStatus
        django_get_or_create = ('title',)

    title = "Done"
    description = "This task is done"
    is_done = True


class PlannedTaskStatusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TaskStatus
        django_get_or_create = ('title',)

    title = "Planned"
    description = "This task is planned"
    is_done = False


class StartedTaskStatusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TaskStatus
        django_get_or_create = ('title',)

    title = "Started"
    description = "This task is started"
    is_done = False
