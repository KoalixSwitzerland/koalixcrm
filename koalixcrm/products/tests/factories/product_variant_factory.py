# -*- coding: utf-8 -*-

import factory

from koalixcrm.products.models.product_variant import ProductVariant
from tests.factories.core.workspace_factory import DefaultWorkspaceFactory
from tests.factories.products.product_type_factory import StandardProductTypeFactory


class StandardProductVariantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductVariant
        django_get_or_create = ('sku',)

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    product = factory.SubFactory(StandardProductTypeFactory)
    sku = "SKU-123456"
    gtin = "01234567890128"
    mpn = "MPN-123456"
    weight_kg = "1.5000"
    dimensions_length_m = "0.1000"
    dimensions_width_m = "0.1000"
    dimensions_height_m = "0.1000"
