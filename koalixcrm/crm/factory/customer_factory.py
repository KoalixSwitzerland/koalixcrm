# -*- coding: utf-8 -*-

import factory
from koalixcrm.crm.models import Customer
from koalixcrm.crm.factory.contact_factory import StandardContactFactory
from koalixcrm.crm.factory.customer_billing_cycle_factory import StandardCustomerBillingCycleFactory


class StandardCustomerFactory(StandardContactFactory):
    class Meta:
        model = Customer

    default_customer_billing_cycle = factory.SubFactory(StandardCustomerBillingCycleFactory)
    is_lead = True

    @factory.post_generation
    def is_member_of(self, create, extracted):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for group in extracted:
                self.is_member_of.add(group)
