# -*- coding: utf-8 -*-

import factory
from koalixcrm.core.models.workspace import Workspace


class DefaultWorkspaceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Workspace
        django_get_or_create = ('name',)

    name = 'Default Workspace'
    is_active = True
