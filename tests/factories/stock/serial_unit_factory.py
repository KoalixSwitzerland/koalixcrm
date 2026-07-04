# -*- coding: utf-8 -*-
import factory

from koalixcrm.stock.models.choices import SerialConditionState
from koalixcrm.stock.models.serial_unit import SerialUnit
from tests.factories.core.workspace_factory import DefaultWorkspaceFactory
from tests.factories.products.product_variant_factory import StandardProductVariantFactory


class StandardSerialUnitFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SerialUnit

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    variant = factory.SubFactory(StandardProductVariantFactory)
    serial_number = factory.Sequence(lambda n: f"SN-{n}")
    condition_state = SerialConditionState.NEW
