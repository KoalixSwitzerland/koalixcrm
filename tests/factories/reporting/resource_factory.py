# -*- coding: utf-8 -*-

import factory

from koalixcrm.reporting.models.resource import Resource
from tests.factories.core.workspace_factory import DefaultWorkspaceFactory
from tests.factories.reporting.resource_manager_factory import (
    StandardResourceManagerFactory,
)
from tests.factories.reporting.resource_type_factory import StandardResourceTypeFactory


class StandardResourceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Resource

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    resource_type = factory.SubFactory(StandardResourceTypeFactory)
    resource_manager = factory.SubFactory(StandardResourceManagerFactory)
