# -*- coding: utf-8 -*-

import factory

from koalixcrm.products.models.product_attribute_mapping import ProductAttributeMapping
from tests.factories.core.workspace_factory import DefaultWorkspaceFactory


class StandardProductAttributeMappingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductAttributeMapping

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    source_standard = "unspsc"
    source_attribute_id = "50000000"
    canonical_key = "koalix.shelf_life_days"
    transform = None
