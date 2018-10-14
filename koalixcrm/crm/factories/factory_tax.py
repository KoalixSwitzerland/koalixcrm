# -*- coding: utf-8 -*-

import factory
from koalixcrm.crm.models import Tax


class StandardTaxFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tax
        django_get_or_create = ('name',)

    tax_rate = "7.7"
    name = "Swiss MwSt 7.7%"
    account_activa = None
    account_passiva = None
