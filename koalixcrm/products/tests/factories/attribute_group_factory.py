# -*- coding: utf-8 -*-

import factory

from koalixcrm.products.models.attribute_group import AttributeGroup
from koalixcrm.products.models.choices import AttributeScope
from koalixcrm.core.tests.factories.workspace_factory import DefaultWorkspaceFactory


class StandardAttributeGroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AttributeGroup
        django_get_or_create = ('workspace', 'key')

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    scope = AttributeScope.WORKSPACE
    key = "nutritional-values"
    name = "Nutritional values per 100g"
    description = "Energy, fat, carbohydrates, protein, salt"
