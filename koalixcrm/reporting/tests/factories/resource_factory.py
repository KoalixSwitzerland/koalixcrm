# -*- coding: utf-8 -*-

import factory

from koalixcrm.reporting.models.resource import Resource
from koalixcrm.core.tests.factories.workspace_factory import DefaultWorkspaceFactory
from koalixcrm.reporting.tests.factories.resource_manager_factory import (
    StandardResourceManagerFactory,
)
from koalixcrm.reporting.tests.factories.resource_type_factory import StandardResourceTypeFactory


class StandardResourceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Resource

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    resource_type = factory.SubFactory(StandardResourceTypeFactory)
    resource_manager = factory.SubFactory(StandardResourceManagerFactory)
