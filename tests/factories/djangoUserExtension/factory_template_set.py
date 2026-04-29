# -*- coding: utf-8 -*-

import factory

from koalixcrm.djangoUserExtension.models import TemplateSet
from tests.factories.core.workspace_factory import DefaultWorkspaceFactory


class StandardTemplateSetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TemplateSet

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    title = "Just an empty Template Set"
