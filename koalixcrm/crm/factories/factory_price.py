# -*- coding: utf-8 -*-

import factory
import datetime
from koalixcrm.crm.models import Price
from koalixcrm.crm.factories.factory_product import StandardProductFactory
from koalixcrm.crm.factories.factory_unit import StandardUnitFactory
from koalixcrm.crm.factories.factory_currency import StandardCurrencyFactory
from koalixcrm.crm.factories.factory_customer_group import StandardCustomerGroupFactory
from koalixcrm.test_support_functions import make_date_utc


class StandardPriceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Price
        django_get_or_create = ('product',
                                'price')

    product = factory.SubFactory(StandardProductFactory)
    unit = factory.SubFactory(StandardUnitFactory)
    currency = factory.SubFactory(StandardCurrencyFactory)
    customer_group = factory.SubFactory(StandardCustomerGroupFactory)
    price = "100.50"
    valid_from = make_date_utc(datetime.datetime(2018, 6, 15, 00))
    valid_until = make_date_utc(datetime.datetime(2024, 6, 15, 00))


class HighPriceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Price
        django_get_or_create = ('product',
                                'price')

    product = factory.SubFactory(StandardProductFactory)
    unit = factory.SubFactory(StandardUnitFactory)
    currency = factory.SubFactory(StandardCurrencyFactory)
    customer_group = factory.SubFactory(StandardCustomerGroupFactory)
    price = "250.50"
    valid_from = make_date_utc(datetime.datetime(2018, 6, 15, 00))
    valid_until = make_date_utc(datetime.datetime(2024, 6, 15, 00))
