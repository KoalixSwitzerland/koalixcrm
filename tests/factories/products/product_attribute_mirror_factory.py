# -*- coding: utf-8 -*-

import factory

from koalixcrm.products.models.product_attribute_mirror import ProductAttributeMirror
from tests.factories.core.workspace_factory import DefaultWorkspaceFactory
from tests.factories.products.product_type_factory import StandardProductTypeFactory


class StandardProductAttributeMirrorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductAttributeMirror

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    product = factory.SubFactory(StandardProductTypeFactory)
    variant = None
    data = factory.LazyFunction(dict)
