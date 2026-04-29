# -*- coding: utf-8 -*-

import factory

from koalixcrm.reporting.models.resource_manager import ResourceManager
from tests.factories.core.workspace_factory import DefaultWorkspaceFactory
from tests.factories.djangoUserExtension.factory_user_extension import (
    StandardUserExtensionFactory,
)


class StandardResourceManagerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ResourceManager

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    user = factory.SubFactory(StandardUserExtensionFactory)
