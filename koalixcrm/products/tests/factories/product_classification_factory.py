# -*- coding: utf-8 -*-

import factory

from koalixcrm.products.models.product_classification import ProductClassification
from koalixcrm.core.tests.factories.workspace_factory import DefaultWorkspaceFactory
from koalixcrm.products.tests.factories.classification_factory import (
    StandardClassificationNodeFactory,
)
from koalixcrm.products.tests.factories.product_type_factory import StandardProductTypeFactory


class StandardProductClassificationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductClassification

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    product = factory.SubFactory(StandardProductTypeFactory)
    classification_node = factory.SubFactory(StandardClassificationNodeFactory)
