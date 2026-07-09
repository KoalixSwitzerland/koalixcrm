# -*- coding: utf-8 -*-

import factory

from koalixcrm.products.models.choices import ProductMediaType
from koalixcrm.products.models.product_media import ProductMedia
from koalixcrm.core.tests.factories.workspace_factory import DefaultWorkspaceFactory
from koalixcrm.products.tests.factories.product_type_factory import StandardProductTypeFactory


class StandardProductMediaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductMedia

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    product = factory.SubFactory(StandardProductTypeFactory)
    media_type = ProductMediaType.IMAGE
    object_key = "products/test-object-key.jpg"
