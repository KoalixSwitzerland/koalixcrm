# -*- coding: utf-8 -*-

import factory
import datetime
from koalixcrm.crm.models import ProductPrice
from koalixcrm.crm.factories.factory_product import StandardProductFactory
from koalixcrm.crm.factories.factory_unit import StandardUnitFactory
from koalixcrm.crm.factories.factory_currency import StandardCurrencyFactory
from koalixcrm.crm.factories.factory_customer_group import StandardCustomerGroupFactory
from koalixcrm.global_support_functions import make_date_utc


class StandardPriceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductPrice
        django_get_or_create = ('product_type',
                                'unit',
                                'currency',
                                'customer_group',
                                'price',
                                'valid_from',
                                'valid_until')

    product_type = factory.SubFactory(StandardProductFactory)
    unit = factory.SubFactory(StandardUnitFactory)
    currency = factory.SubFactory(StandardCurrencyFactory)
    customer_group = factory.SubFactory(StandardCustomerGroupFactory)
    price = "100.50"
    valid_from = make_date_utc(datetime.datetime(2018, 6, 15, 00)).date()
    valid_until = make_date_utc(datetime.datetime(2024, 6, 15, 00)).date()


class HighPriceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductPrice
    product_type = factory.SubFactory(StandardProductFactory)
    unit = factory.SubFactory(StandardUnitFactory)
    currency = factory.SubFactory(StandardCurrencyFactory)
    customer_group = factory.SubFactory(StandardCustomerGroupFactory)
    price = "250.50"
    valid_from = make_date_utc(datetime.datetime(2018, 6, 15, 00)).date()
    valid_until = make_date_utc(datetime.datetime(2024, 6, 15, 00)).date()
