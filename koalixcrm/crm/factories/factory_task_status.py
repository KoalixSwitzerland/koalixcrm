# -*- coding: utf-8 -*-

import factory
from koalixcrm.crm.models import TaskStatus


class DoneTaskStatusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TaskStatus

    title = "Done"
    description = "This task is done"
    is_done = True
