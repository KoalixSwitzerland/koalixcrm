# -*- coding: utf-8 -*-

import factory
import datetime
from koalixcrm.reporting.models.resource_price import ResourcePrice
from tests.factories.reporting.resource_factory import StandardResourceFactory
from tests.factories.settings.unit_factory import StandardUnitFactory
from tests.factories.settings.currency_factory import StandardCurrencyFactory
from tests.factories.crm.customer_group_factory import StandardCustomerGroupFactory
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
