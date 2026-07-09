# -*- coding: utf-8 -*-

import factory

from koalixcrm.products.models.attribute_set_default import AttributeSetDefault
from tests.factories.core.workspace_factory import DefaultWorkspaceFactory
from tests.factories.products.attribute_definition_factory import (
    StandardAttributeDefinitionFactory,
)
from tests.factories.products.attribute_set_factory import StandardAttributeSetFactory


class StandardAttributeSetDefaultFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AttributeSetDefault

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    attribute_set = factory.SubFactory(StandardAttributeSetFactory)
    attribute_definition = factory.SubFactory(StandardAttributeDefinitionFactory)
    default_value = "matt"
