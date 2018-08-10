# -*- coding: utf-8 -*-

import factory
from koalixcrm.crm.models import ProjectStatus


class DoneProjectStatusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProjectStatus

    title = "Done"
    description = "This project is done"
    is_done = True


class StartedProjectStatusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProjectStatus

    title = "Started"
    description = "This project has started"
    is_done = False
