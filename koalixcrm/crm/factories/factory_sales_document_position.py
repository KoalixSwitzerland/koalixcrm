# -*- coding: utf-8 -*-

import factory
from koalixcrm.crm.models import SalesDocumentPosition
from koalixcrm.crm.factories.factory_product_type import StandardProductTypeFactory
from koalixcrm.crm.factories.factory_unit import StandardUnitFactory


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

