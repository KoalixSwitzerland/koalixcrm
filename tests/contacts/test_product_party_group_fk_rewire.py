# -*- coding: utf-8 -*-
"""Verify the products.Price / CustomerGroupTransform Party-group FK rewire
(issue #394, Phase B).
"""
from decimal import Decimal

from django.apps import apps as live_apps
from django.test import TestCase

from koalixcrm.contacts.backfill import (
    build_legacy_customer_group_to_party_group_mapping,
    forwards,
)
from koalixcrm.contacts.models.customer_group import CustomerGroup as LegacyCustomerGroup
from koalixcrm.contacts.models.party_group import PartyGroup
from koalixcrm.core.models.currency import Currency
from koalixcrm.core.models.unit import Unit
from koalixcrm.products.models.price import Price
from koalixcrm.products.party_group_fk_rewire import populate_party_group_fks


class ProductPartyGroupFKRewireTest(TestCase):
    def setUp(self):
        self.unit = Unit.objects.create(description='Each', short_name='ea')
        self.currency = Currency.objects.create(
            description='Swiss Franc', short_name='CHF', rounding='0.05',
        )
        self.group_a = LegacyCustomerGroup.objects.create(name='Group A')
        self.group_b = LegacyCustomerGroup.objects.create(name='Group B')

        self.price_with_group = Price.objects.create(
            unit=self.unit, currency=self.currency,
            customer_group=self.group_a,
            price=Decimal('100.00'),
        )
        self.price_without_group = Price.objects.create(
            unit=self.unit, currency=self.currency,
            price=Decimal('42.00'),
        )

    def test_customer_group_mapping(self):
        forwards(live_apps, None)

        mapping = build_legacy_customer_group_to_party_group_mapping(live_apps)

        self.assertEqual(len(mapping), 2)
        # Each legacy group maps to a PartyGroup whose name matches.
        for legacy_id, pg_id in mapping.items():
            pg = PartyGroup.objects.get(id=pg_id)
            self.assertEqual(pg.name, LegacyCustomerGroup.objects.get(id=legacy_id).name)
            self.assertEqual(pg.role_type_scope, 'customer')

    def test_price_party_group_populated(self):
        forwards(live_apps, None)
        populate_party_group_fks(live_apps, None)

        self.price_with_group.refresh_from_db()
        self.price_without_group.refresh_from_db()

        self.assertIsNotNone(self.price_with_group.party_group_id)
        self.assertEqual(
            self.price_with_group.party_group.name, self.group_a.name,
        )
        self.assertIsNone(self.price_without_group.party_group_id)
        # Legacy FK untouched.
        self.assertEqual(self.price_with_group.customer_group_id, self.group_a.id)
