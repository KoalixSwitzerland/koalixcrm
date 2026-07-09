# -*- coding: utf-8 -*-

import factory

from koalixcrm.products.models.product_classification import ProductClassification
from tests.factories.core.workspace_factory import DefaultWorkspaceFactory
from tests.factories.products.classification_factory import (
    StandardClassificationNodeFactory,
)
from tests.factories.products.product_type_factory import StandardProductTypeFactory


class StandardProductClassificationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductClassification

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    product = factory.SubFactory(StandardProductTypeFactory)
    classification_node = factory.SubFactory(StandardClassificationNodeFactory)
