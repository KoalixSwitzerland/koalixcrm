# -*- coding: utf-8 -*-

import factory

from koalixcrm.products.models.attribute_definition import AttributeDefinition
from koalixcrm.products.models.choices import AttributeDataType, AttributeScope
from koalixcrm.core.tests.factories.workspace_factory import DefaultWorkspaceFactory
from koalixcrm.products.tests.factories.attribute_group_factory import (
    StandardAttributeGroupFactory,
)


class StandardAttributeDefinitionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AttributeDefinition
        django_get_or_create = ('workspace', 'key')

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    scope = AttributeScope.WORKSPACE
    key = "gloss_level"
    label = "Gloss Level"
    data_type = AttributeDataType.ENUM
    enum_values = ["matt", "satin", "gloss"]
    group = factory.SubFactory(StandardAttributeGroupFactory)
