# -*- coding: utf-8 -*-

import factory

from koalixcrm.products.models.product_attribute_mirror import ProductAttributeMirror
from koalixcrm.core.tests.factories.workspace_factory import DefaultWorkspaceFactory
from koalixcrm.products.tests.factories.product_type_factory import StandardProductTypeFactory


class StandardProductAttributeMirrorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductAttributeMirror

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    product = factory.SubFactory(StandardProductTypeFactory)
    variant = None
    data = factory.LazyFunction(dict)
