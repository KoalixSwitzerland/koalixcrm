# -*- coding: utf-8 -*-

import factory
from koalixcrm.crm.models import CustomerBillingCycle


class StandardCustomerBillingCycleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomerBillingCycle
        django_get_or_create = ('name',)

    name = "This is a test billing cycle"
    time_to_payment_date = 30
    payment_reminder_time_to_payment = 20
