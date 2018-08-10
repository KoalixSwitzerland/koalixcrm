# -*- coding: utf-8 -*-

import factory
from koalixcrm.crm.models import ProjectLinkType


class RelatedToProjectLinkTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProjectLinkType

    title = "Is related to"
    description = "This project is related with ...."


class RequiresProjectLinkTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProjectLinkType

    title = "This project requires"
    description = "This project requires the completion or the existence of ...."
