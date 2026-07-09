# -*- coding: utf-8 -*-

import factory

from koalixcrm.reporting.models.human_resource import HumanResource
from koalixcrm.core.tests.factories.workspace_factory import DefaultWorkspaceFactory
from koalixcrm.djangoUserExtension.tests.factories.user_extension_factory import (
    StandardUserExtensionFactory,
)
from koalixcrm.reporting.tests.factories.resource_manager_factory import (
    StandardResourceManagerFactory,
)
from koalixcrm.reporting.tests.factories.resource_type_factory import StandardResourceTypeFactory


class StandardHumanResourceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = HumanResource

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    user = factory.SubFactory(StandardUserExtensionFactory)
    resource_type = factory.SubFactory(StandardResourceTypeFactory)
    resource_manager = factory.SubFactory(StandardResourceManagerFactory)
