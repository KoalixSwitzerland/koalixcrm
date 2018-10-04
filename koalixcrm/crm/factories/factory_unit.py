# -*- coding: utf-8 -*-

import factory
from koalixcrm.crm.models import Unit


class StandardUnitFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Unit
        django_get_or_create = ('short_name',)

    description = "Kilogram"
    short_name = "kg"
    is_a_fraction_of = None
    fraction_factor_to_next_higher_unit = None


class SmallUnitFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Unit
        django_get_or_create = ('short_name',)

    description = "Gram"
    short_name = "g"
    is_a_fraction_of = factory.SubFactory(StandardUnitFactory)
    fraction_factor_to_next_higher_unit = 1000
