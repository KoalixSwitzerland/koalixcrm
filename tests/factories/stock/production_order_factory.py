# -*- coding: utf-8 -*-
import factory

from koalixcrm.stock.models.production_order import ProductionOrder
from koalixcrm.stock.models.production_order_component import ProductionOrderComponent
from tests.factories.core.unit_factory import StandardUnitFactory
from tests.factories.core.workspace_factory import DefaultWorkspaceFactory
from tests.factories.products.bill_of_materials_factory import StandardBillOfMaterialsFactory


class StandardProductionOrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductionOrder

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    bill_of_materials = factory.SubFactory(StandardBillOfMaterialsFactory)
    product = factory.LazyAttribute(lambda o: o.bill_of_materials.product)
    planned_qty = "5.0000"
    uom = factory.SubFactory(StandardUnitFactory)


class StandardProductionOrderComponentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductionOrderComponent

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    production_order = factory.SubFactory(StandardProductionOrderFactory)
    planned_qty = "10.0000"
    uom = factory.SubFactory(StandardUnitFactory)
