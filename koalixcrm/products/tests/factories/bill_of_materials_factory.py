# -*- coding: utf-8 -*-

import factory

from koalixcrm.products.models.bill_of_materials import BillOfMaterials
from koalixcrm.products.models.bom_item import BomItem
from koalixcrm.products.models.choices import ProductKind
from tests.factories.core.unit_factory import StandardUnitFactory
from tests.factories.core.workspace_factory import DefaultWorkspaceFactory
from tests.factories.products.product_type_factory import StandardProductTypeFactory


class StandardBillOfMaterialsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BillOfMaterials
        django_get_or_create = ('product',)

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    product = factory.SubFactory(
        StandardProductTypeFactory,
        kind=ProductKind.MANUFACTURED_GOOD,
        product_type_identifier=factory.Sequence(lambda n: f"BOM-PARENT-{n}"),
    )
    name = "Standard BOM"
    description = "Test bill of materials"


class StandardBomItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BomItem

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    bill_of_materials = factory.SubFactory(StandardBillOfMaterialsFactory)
    component_product = factory.SubFactory(
        StandardProductTypeFactory,
        kind=ProductKind.RAW_MATERIAL,
        product_type_identifier=factory.Sequence(lambda n: f"BOM-COMPONENT-{n}"),
    )
    quantity = "2.0000"
    unit = factory.SubFactory(StandardUnitFactory)
    scrap_pct = "5.00"
    alternative_component = None
    default_component_variant = None
