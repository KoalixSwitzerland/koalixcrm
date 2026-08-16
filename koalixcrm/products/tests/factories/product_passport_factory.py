# -*- coding: utf-8 -*-

import factory

from koalixcrm.products.models.product_passport import ProductPassport
from koalixcrm.core.tests.factories.workspace_factory import DefaultWorkspaceFactory
from koalixcrm.products.tests.factories.product_type_factory import StandardProductTypeFactory


class StandardProductPassportFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductPassport
        django_get_or_create = ('product',)

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    product = factory.SubFactory(StandardProductTypeFactory)
    passport_data = factory.LazyFunction(dict)
