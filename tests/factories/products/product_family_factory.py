# -*- coding: utf-8 -*-

import factory

from koalixcrm.products.models.product_family import ProductFamily
from tests.factories.core.workspace_factory import DefaultWorkspaceFactory


class StandardProductFamilyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductFamily

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    name = "This is a test Product Family"
    description = "This is a test Product Family"
