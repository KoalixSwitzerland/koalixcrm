# -*- coding: utf-8 -*-

import factory
from koalixcrm.contracts.models.sales_document_position import SalesDocumentPosition
from koalixcrm.products.factory.product_type_factory import StandardProductTypeFactory
from koalixcrm.settings.factory.unit_factory import StandardUnitFactory


class StandardSalesDocumentPositionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SalesDocumentPosition

    position_number = 5
    quantity = 5
    description = "This is a test sales document position"
    discount = 10
    product_type = factory.SubFactory(StandardProductTypeFactory)
    unit = factory.SubFactory(StandardUnitFactory)
    overwrite_product_price = True
    position_price_per_unit = 155
