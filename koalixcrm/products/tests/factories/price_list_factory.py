# -*- coding: utf-8 -*-

import factory

from koalixcrm.products.models.price_list import PriceList
from koalixcrm.core.tests.factories.workspace_factory import DefaultWorkspaceFactory


class StandardPriceListFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PriceList
        django_get_or_create = ('workspace', 'name')

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    name = factory.Sequence(lambda n: f"Standard Price List {n}")
    channel = "webshop"
    party_group = None
    description = "Test price list"
