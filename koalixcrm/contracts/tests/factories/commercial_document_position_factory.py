# -*- coding: utf-8 -*-

import factory

from koalixcrm.contracts.models.commercial_document_position import (
    CommercialDocumentPosition,
)
from koalixcrm.core.tests.factories.unit_factory import StandardUnitFactory
from koalixcrm.core.tests.factories.workspace_factory import DefaultWorkspaceFactory
from koalixcrm.products.tests.factories.product_type_factory import StandardProductTypeFactory


class StandardCommercialDocumentPositionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CommercialDocumentPosition

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    position_number = 5
    quantity = 5
    description = "This is a test commercial document position"
    discount = 10
    product_type = factory.SubFactory(StandardProductTypeFactory)
    unit = factory.SubFactory(StandardUnitFactory)
    overwrite_product_price = True
    position_price_per_unit = 155
