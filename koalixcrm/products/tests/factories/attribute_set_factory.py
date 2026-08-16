# -*- coding: utf-8 -*-

import factory

from koalixcrm.products.models.attribute_set import AttributeSet, AttributeSetGroup
from koalixcrm.core.tests.factories.workspace_factory import DefaultWorkspaceFactory
from koalixcrm.products.tests.factories.attribute_group_factory import (
    StandardAttributeGroupFactory,
)


class StandardAttributeSetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AttributeSet

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    name = "Coatings"
    kind = None
    classification_node = None
    product_family = None


class StandardAttributeSetGroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AttributeSetGroup

    attribute_set = factory.SubFactory(StandardAttributeSetFactory)
    attribute_group = factory.SubFactory(StandardAttributeGroupFactory)
    order = 0
