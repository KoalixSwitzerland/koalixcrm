# -*- coding: utf-8 -*-

import factory

from koalixcrm.products.models.unit_of_measure_conversion import (
    UnitOfMeasureConversion,
)
from koalixcrm.core.tests.factories.unit_factory import SmallUnitFactory, StandardUnitFactory
from koalixcrm.core.tests.factories.workspace_factory import DefaultWorkspaceFactory
from koalixcrm.products.tests.factories.product_type_factory import StandardProductTypeFactory


class StandardUnitOfMeasureConversionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UnitOfMeasureConversion
        django_get_or_create = ('product', 'from_unit', 'to_unit')

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    product = factory.SubFactory(StandardProductTypeFactory)
    from_unit = factory.SubFactory(StandardUnitFactory)
    to_unit = factory.SubFactory(SmallUnitFactory)
    factor = "1000.0000000000"
