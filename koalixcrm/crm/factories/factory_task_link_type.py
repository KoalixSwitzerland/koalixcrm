# -*- coding: utf-8 -*-

import factory
from koalixcrm.crm.models import TaskLinkType


class RelatedToTaskLinkTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TaskLinkType

    title = "Is related to"
    description = "This task is related with ...."


class RequiresLinkTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TaskLinkType

    title = "This task requires"
    description = "This task requires the completion or the existence of ...."
