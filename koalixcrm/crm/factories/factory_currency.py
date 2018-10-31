# -*- coding: utf-8 -*-

import factory
from koalixcrm.crm.models import Currency


class StandardCurrencyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Currency
        django_get_or_create = ('description',)

    description = "Swiss Francs"
    short_name = "CHF"
    rounding = "0.05"


class SecondStandardCurrencyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Currency
        django_get_or_create = ('description',)

    description = "Euro"
    short_name = "EUR"
    rounding = "0.01"
