# -*- coding: utf-8 -*-

import factory

from koalixcrm.contacts.models import CustomerBillingCycle
from koalixcrm.core.tests.factories.workspace_factory import DefaultWorkspaceFactory


class StandardCustomerBillingCycleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomerBillingCycle
        django_get_or_create = ('name',)

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    name = "This is a test billing cycle"
    time_to_payment_date = 30
    payment_reminder_time_to_payment = 20
