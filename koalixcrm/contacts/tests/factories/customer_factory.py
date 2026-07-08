# -*- coding: utf-8 -*-
"""Customer-role factory (post-v2.0.0 / issue #395 G3).

Creates an Organization with an active `customer` PartyRole and the
`default_billing_cycle` set — the v2.0.0 equivalent of the legacy
Customer model. Tests that assert legacy-Customer-only attributes
(`is_lead`, `is_member_of`, …) need to be ported to the new shape.
"""
import factory

from koalixcrm.contacts.models.party_group_membership import PartyGroupMembership
from koalixcrm.contacts.models.party_role import PartyRole
from koalixcrm.contacts.tests.factories.contact_factory import StandardContactFactory
from koalixcrm.contacts.tests.factories.customer_billing_cycle_factory import (
    StandardCustomerBillingCycleFactory,
)


class StandardCustomerFactory(StandardContactFactory):
    default_billing_cycle = factory.SubFactory(StandardCustomerBillingCycleFactory)

    @factory.post_generation
    def customer_role(obj, create, extracted, **kwargs):
        if not create:
            return
        # ISO string instead of date() — some tests freeze datetime.date and
        # breaks Django's isinstance check for DateField values.
        PartyRole.objects.create(
            party_id=obj.pk,
            role_type='customer',
            is_primary=True,
            valid_from='1970-01-01',
            workspace=obj.workspace,
        )

    @factory.post_generation
    def is_member_of(obj, create, extracted, **kwargs):
        """Accepts an iterable of PartyGroup (or legacy kwarg alias) and
        creates PartyGroupMembership rows — v2.0.0 replacement for the
        legacy Contact.is_member_of M2M."""
        if not create or not extracted:
            return
        for group in extracted:
            PartyGroupMembership.objects.create(party_id=obj.pk, party_group=group, workspace=obj.workspace)
