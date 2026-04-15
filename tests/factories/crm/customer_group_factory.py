# -*- coding: utf-8 -*-

import factory
from koalixcrm.crm.models import CustomerGroup


class StandardCustomerGroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomerGroup
        django_get_or_create = ('name',)

    name = factory.Sequence(lambda n: "Customer Group #%s" % n)


class AdvancedCustomerGroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomerGroup

    name = factory.Sequence(lambda n: "Customer Group #%s" % n)
