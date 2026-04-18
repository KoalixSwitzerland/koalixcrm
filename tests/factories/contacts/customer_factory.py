# -*- coding: utf-8 -*-
"""Customer-role factory (post-v2.0.0 / issue #395 G3).

Creates an Organization with an active `customer` PartyRole and the
`default_billing_cycle` set — the v2.0.0 equivalent of the legacy
Customer model. Tests that assert legacy-Customer-only attributes
(`is_lead`, `is_member_of`, …) need to be ported to the new shape.
"""
from datetime import date

import factory

from koalixcrm.contacts.models.party_role import PartyRole
from tests.factories.contacts.contact_factory import StandardContactFactory
from tests.factories.contacts.customer_billing_cycle_factory import (
    StandardCustomerBillingCycleFactory,
)


class StandardCustomerFactory(StandardContactFactory):
    default_billing_cycle = factory.SubFactory(StandardCustomerBillingCycleFactory)

    @factory.post_generation
    def customer_role(obj, create, extracted, **kwargs):
        if not create:
            return
        PartyRole.objects.create(
            party_id=obj.pk,
            role_type='customer',
            is_primary=True,
            valid_from=date(1970, 1, 1),
        )
