# -*- coding: utf-8 -*-

import factory

from koalixcrm.products.models.product_translation import ProductTranslation
from koalixcrm.core.tests.factories.workspace_factory import DefaultWorkspaceFactory
from koalixcrm.products.tests.factories.product_type_factory import StandardProductTypeFactory


class StandardProductTranslationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductTranslation
        django_get_or_create = ('product', 'language_code')

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    product = factory.SubFactory(StandardProductTypeFactory)
    language_code = "en"
    name = "This is a test Product Translation"
    short_description = "Short description"
    long_description = "Long description"
