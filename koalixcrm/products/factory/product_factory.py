# -*- coding: utf-8 -*-

import factory
from koalixcrm.products.models.product import Product


class StandardProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product
        django_get_or_create = ('product_number',)
