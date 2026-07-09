# -*- coding: utf-8 -*-

import factory

from koalixcrm.products.models.classification import Classification, ClassificationNode


class StandardClassificationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Classification
        django_get_or_create = ('code',)

    code = "unspsc"
    name = "UNSPSC"
    description = "United Nations Standard Products and Services Code"


class StandardClassificationNodeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ClassificationNode

    classification = factory.SubFactory(StandardClassificationFactory)
    parent = None
    code = "50000000"
    name = "Food, Beverage and Tobacco Products"
    level = 1
