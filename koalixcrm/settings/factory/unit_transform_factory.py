# -*- coding: utf-8 -*-

import factory
from koalixcrm.settings.models.unit_transform import UnitTransform
from koalixcrm.settings.factory.unit_factory import StandardUnitFactory, SmallUnitFactory
from koalixcrm.products.factory.product_type_factory import StandardProductTypeFactory


class StandardUnitTransformFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UnitTransform
        django_get_or_create = ('from_unit',
                                'to_unit')

    from_unit = factory.SubFactory(StandardUnitFactory)
    to_unit = factory.SubFactory(SmallUnitFactory)
    product_type = factory.SubFactory(StandardProductTypeFactory)
    factor = 1.10
