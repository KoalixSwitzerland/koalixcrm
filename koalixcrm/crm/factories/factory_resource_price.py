# -*- coding: utf-8 -*-

import factory
import datetime
from koalixcrm.crm.models import ResourcePrice
from koalixcrm.crm.factories.factory_resource import StandardResourceFactory
from koalixcrm.crm.factories.factory_unit import StandardUnitFactory
from koalixcrm.crm.factories.factory_currency import StandardCurrencyFactory
from koalixcrm.crm.factories.factory_customer_group import StandardCustomerGroupFactory
from koalixcrm.global_support_functions import make_date_utc


class StandardResourcePriceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ResourcePrice

    resource = factory.SubFactory(StandardResourceFactory)
    unit = factory.SubFactory(StandardUnitFactory)
    currency = factory.SubFactory(StandardCurrencyFactory)
    customer_group = factory.SubFactory(StandardCustomerGroupFactory)
    price = "100.50"
    valid_from = make_date_utc(datetime.datetime(2018, 6, 15, 00))
    valid_until = make_date_utc(datetime.datetime(2024, 6, 15, 00))


class HighResourcePriceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ResourcePrice

    resource = factory.SubFactory(StandardResourceFactory)
    unit = factory.SubFactory(StandardUnitFactory)
    currency = factory.SubFactory(StandardCurrencyFactory)
    customer_group = factory.SubFactory(StandardCustomerGroupFactory)
    price = "250.50"
    valid_from = make_date_utc(datetime.datetime(2018, 6, 15, 00))
    valid_until = make_date_utc(datetime.datetime(2024, 6, 15, 00))
