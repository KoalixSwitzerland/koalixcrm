# -*- coding: utf-8 -*-

import datetime

import factory

from koalixcrm.global_support_functions import make_date_utc
from koalixcrm.reporting.models.resource_price import ResourcePrice
from koalixcrm.contacts.tests.factories.customer_group_factory import StandardCustomerGroupFactory
from koalixcrm.core.tests.factories.currency_factory import StandardCurrencyFactory
from koalixcrm.core.tests.factories.unit_factory import StandardUnitFactory
from koalixcrm.core.tests.factories.workspace_factory import DefaultWorkspaceFactory
from koalixcrm.reporting.tests.factories.resource_factory import StandardResourceFactory


class StandardResourcePriceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ResourcePrice

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    resource = factory.SubFactory(StandardResourceFactory)
    unit = factory.SubFactory(StandardUnitFactory)
    currency = factory.SubFactory(StandardCurrencyFactory)
    party_group = factory.SubFactory(StandardCustomerGroupFactory)
    price = "100.50"
    valid_from = make_date_utc(datetime.datetime(2018, 6, 15, 00))
    valid_until = make_date_utc(datetime.datetime(2024, 6, 15, 00))


class HighResourcePriceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ResourcePrice

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    resource = factory.SubFactory(StandardResourceFactory)
    unit = factory.SubFactory(StandardUnitFactory)
    currency = factory.SubFactory(StandardCurrencyFactory)
    party_group = factory.SubFactory(StandardCustomerGroupFactory)
    price = "250.50"
    valid_from = make_date_utc(datetime.datetime(2018, 6, 15, 00))
    valid_until = make_date_utc(datetime.datetime(2024, 6, 15, 00))
