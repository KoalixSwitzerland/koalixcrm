# -*- coding: utf-8 -*-

import factory
from koalixcrm.crm.models import CurrencyTransform
from koalixcrm.crm.factories.factory_currency import StandardCurrencyFactory, SecondStandardCurrencyFactory
from koalixcrm.crm.factories.factory_product_type import StandardProductTypeFactory


class StandardCurrencyTransformFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CurrencyTransform
        django_get_or_create = ('from_currency',
                                'to_currency')

    from_currency = factory.SubFactory(StandardCurrencyFactory)
    to_currency = factory.SubFactory(SecondStandardCurrencyFactory)
    product_type = factory.SubFactory(StandardProductTypeFactory)
    factor = 0.90
