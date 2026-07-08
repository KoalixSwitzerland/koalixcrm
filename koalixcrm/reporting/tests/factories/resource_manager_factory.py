# -*- coding: utf-8 -*-

import factory

from koalixcrm.reporting.models.resource_manager import ResourceManager
from koalixcrm.core.tests.factories.workspace_factory import DefaultWorkspaceFactory
from koalixcrm.djangoUserExtension.tests.factories.user_extension_factory import (
    StandardUserExtensionFactory,
)


class StandardResourceManagerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ResourceManager

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    user = factory.SubFactory(StandardUserExtensionFactory)
