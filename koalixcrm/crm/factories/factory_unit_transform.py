# -*- coding: utf-8 -*-

import factory
from koalixcrm.crm.models import UnitTransform
from koalixcrm.crm.factories.factory_unit import StandardUnitFactory, SmallUnitFactory
from koalixcrm.crm.factories.factory_product_type import StandardProductTypeFactory


class StandardUnitTransformFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UnitTransform
        django_get_or_create = ('from_unit',
                                'to_unit')

    from_unit = factory.SubFactory(StandardUnitFactory)
    to_unit = factory.SubFactory(SmallUnitFactory)
    product_type = factory.SubFactory(StandardProductTypeFactory)
    factor = 1.10
