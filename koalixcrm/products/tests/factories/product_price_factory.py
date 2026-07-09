# -*- coding: utf-8 -*-

import datetime

import factory

from koalixcrm.global_support_functions import make_date_utc
from koalixcrm.products.models.product_price import ProductPrice
from koalixcrm.contacts.tests.factories.customer_group_factory import StandardCustomerGroupFactory
from koalixcrm.core.tests.factories.currency_factory import StandardCurrencyFactory
from koalixcrm.core.tests.factories.unit_factory import StandardUnitFactory
from koalixcrm.core.tests.factories.workspace_factory import DefaultWorkspaceFactory
from koalixcrm.products.tests.factories.product_factory import StandardProductFactory


class StandardPriceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductPrice
        django_get_or_create = ('product_type',
                                'unit',
                                'currency',
                                'party_group',
                                'price',
                                'valid_from',
                                'valid_until')

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    product_type = factory.SubFactory(StandardProductFactory)
    unit = factory.SubFactory(StandardUnitFactory)
    currency = factory.SubFactory(StandardCurrencyFactory)
    party_group = factory.SubFactory(StandardCustomerGroupFactory)
    price = "100.50"
    valid_from = make_date_utc(datetime.datetime(2018, 6, 15, 00)).date()
    valid_until = make_date_utc(datetime.datetime(2024, 6, 15, 00)).date()


class HighPriceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductPrice

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    product_type = factory.SubFactory(StandardProductFactory)
    unit = factory.SubFactory(StandardUnitFactory)
    currency = factory.SubFactory(StandardCurrencyFactory)
    party_group = factory.SubFactory(StandardCustomerGroupFactory)
    price = "250.50"
    valid_from = make_date_utc(datetime.datetime(2018, 6, 15, 00)).date()
    valid_until = make_date_utc(datetime.datetime(2024, 6, 15, 00)).date()
