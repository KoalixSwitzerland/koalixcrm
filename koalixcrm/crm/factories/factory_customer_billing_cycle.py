# -*- coding: utf-8 -*-

import factory
from koalixcrm.crm.models import CustomerBillingCycle


class StandardCustomerBillingCycleFactory(factory.Factory):
    class Meta:
        model = CustomerBillingCycle

    name = "This is a test billing cycle"
    time_to_payment_date = 30
    payment_reminder_time_to_payment = 20
