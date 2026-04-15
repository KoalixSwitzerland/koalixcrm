# -*- coding: utf-8 -*-

import factory
from koalixcrm.settings.models.currency_transform import CurrencyTransform
from koalixcrm.settings.factory.currency_factory import StandardCurrencyFactory, SecondStandardCurrencyFactory
from koalixcrm.products.factory.product_type_factory import StandardProductTypeFactory


class StandardCurrencyTransformFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CurrencyTransform
        django_get_or_create = ('from_currency',
                                'to_currency')

    from_currency = factory.SubFactory(StandardCurrencyFactory)
    to_currency = factory.SubFactory(SecondStandardCurrencyFactory)
    product_type = factory.SubFactory(StandardProductTypeFactory)
    factor = 0.90
