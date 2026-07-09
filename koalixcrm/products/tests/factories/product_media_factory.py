# -*- coding: utf-8 -*-

import factory

from koalixcrm.products.models.choices import ProductMediaType
from koalixcrm.products.models.product_media import ProductMedia
from tests.factories.core.workspace_factory import DefaultWorkspaceFactory
from tests.factories.products.product_type_factory import StandardProductTypeFactory


class StandardProductMediaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductMedia

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    product = factory.SubFactory(StandardProductTypeFactory)
    media_type = ProductMediaType.IMAGE
    object_key = "products/test-object-key.jpg"
