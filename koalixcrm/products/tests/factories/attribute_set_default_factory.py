# -*- coding: utf-8 -*-

import factory

from koalixcrm.products.models.attribute_set_default import AttributeSetDefault
from koalixcrm.core.tests.factories.workspace_factory import DefaultWorkspaceFactory
from koalixcrm.products.tests.factories.attribute_definition_factory import (
    StandardAttributeDefinitionFactory,
)
from koalixcrm.products.tests.factories.attribute_set_factory import StandardAttributeSetFactory


class StandardAttributeSetDefaultFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AttributeSetDefault

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    attribute_set = factory.SubFactory(StandardAttributeSetFactory)
    attribute_definition = factory.SubFactory(StandardAttributeDefinitionFactory)
    default_value = "matt"
