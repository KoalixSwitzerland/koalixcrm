# -*- coding: utf-8 -*-

import factory

from koalixcrm.products.models.unit_of_measure_conversion import (
    UnitOfMeasureConversion,
)
from tests.factories.core.unit_factory import SmallUnitFactory, StandardUnitFactory
from tests.factories.core.workspace_factory import DefaultWorkspaceFactory
from tests.factories.products.product_type_factory import StandardProductTypeFactory


class StandardUnitOfMeasureConversionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UnitOfMeasureConversion
        django_get_or_create = ('product', 'from_unit', 'to_unit')

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    product = factory.SubFactory(StandardProductTypeFactory)
    from_unit = factory.SubFactory(StandardUnitFactory)
    to_unit = factory.SubFactory(SmallUnitFactory)
    factor = "1000.0000000000"
