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
