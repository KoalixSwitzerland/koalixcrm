# -*- coding: utf-8 -*-
import factory

from koalixcrm.stock.models.stock_balance import StockBalance
from tests.factories.core.unit_factory import StandardUnitFactory
from tests.factories.core.workspace_factory import DefaultWorkspaceFactory
from tests.factories.products.product_variant_factory import StandardProductVariantFactory
from tests.factories.stock.location_factory import StandardLocationFactory


class StandardStockBalanceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = StockBalance

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    variant = factory.SubFactory(StandardProductVariantFactory)
    location = factory.SubFactory(StandardLocationFactory)
    uom = factory.SubFactory(StandardUnitFactory)
