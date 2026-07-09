# -*- coding: utf-8 -*-
import factory

from koalixcrm.stock.models.stock_balance import StockBalance
from koalixcrm.core.tests.factories.unit_factory import StandardUnitFactory
from koalixcrm.core.tests.factories.workspace_factory import DefaultWorkspaceFactory
from koalixcrm.products.tests.factories.product_variant_factory import StandardProductVariantFactory
from koalixcrm.stock.tests.factories.location_factory import StandardLocationFactory


class StandardStockBalanceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = StockBalance

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    variant = factory.SubFactory(StandardProductVariantFactory)
    location = factory.SubFactory(StandardLocationFactory)
    uom = factory.SubFactory(StandardUnitFactory)
