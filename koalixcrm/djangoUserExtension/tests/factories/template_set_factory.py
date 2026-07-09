# -*- coding: utf-8 -*-

import factory

from koalixcrm.djangoUserExtension.models import TemplateSet
from koalixcrm.core.tests.factories.workspace_factory import DefaultWorkspaceFactory


class StandardTemplateSetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TemplateSet

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    title = "Just an empty Template Set"
