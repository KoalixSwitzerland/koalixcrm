# -*- coding: utf-8 -*-
"""Supplier-role factory (post-v2.0.0 / issue #395 G3).

Creates an Organization with an active `supplier` PartyRole — the v2.0.0
equivalent of the legacy Supplier model. `offers_shipment_to_customers`
has no direct replacement in the Party pattern; tests that depended on
it need a follow-up.
"""
import factory

from koalixcrm.contacts.models.party_role import PartyRole
from koalixcrm.contacts.tests.factories.contact_factory import StandardContactFactory


class StandardSupplierFactory(StandardContactFactory):

    @factory.post_generation
    def supplier_role(obj, create, extracted, **kwargs):
        if not create:
            return
        # ISO string instead of date() — some tests freeze datetime.date and
        # breaks Django's isinstance check for DateField values.
        PartyRole.objects.create(
            party_id=obj.pk,
            role_type='supplier',
            is_primary=True,
            valid_from='1970-01-01',
            workspace=obj.workspace,
        )
