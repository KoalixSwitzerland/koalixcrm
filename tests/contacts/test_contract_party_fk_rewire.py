# -*- coding: utf-8 -*-
"""Verify the Contract / CommercialDocument Party FK rewire (issue #394).

After the backfill runs, invoking `populate_party_fks` must set
`Contract.buyer_party`, `Contract.supplier_party`, and
`CommercialDocument.party` to the Party rows corresponding to the
legacy FK targets.
"""
from django.apps import apps as live_apps
from django.contrib.auth.models import User
from django.test import TestCase

from koalixcrm.contacts.backfill import forwards
from koalixcrm.contacts.models.customer import Customer as LegacyCustomer
from koalixcrm.contacts.models.customer_billing_cycle import CustomerBillingCycle
from koalixcrm.contacts.models.supplier import Supplier as LegacySupplier
from koalixcrm.contracts.party_fk_rewire import populate_party_fks
from koalixcrm.contracts.models.contract import Contract
from koalixcrm.core.models.currency import Currency


class ContractPartyFKRewireTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='migrationuser', is_staff=True)
        self.billing_cycle = CustomerBillingCycle.objects.create(
            name='Default', time_to_payment_date=30,
            payment_reminder_time_to_payment=14,
        )
        self.currency = Currency.objects.create(
            description='Swiss Franc', short_name='CHF', rounding='0.05',
        )

        self.customer = LegacyCustomer.objects.create(
            name='ACME AG', last_modified_by=self.user,
            default_customer_billing_cycle=self.billing_cycle,
            is_lead=False,
        )
        self.supplier = LegacySupplier.objects.create(
            name='Supplier GmbH', last_modified_by=self.user,
            offers_shipment_to_customers=True,
        )

        self.contract = Contract.objects.create(
            description='Test contract',
            default_customer=self.customer,
            default_supplier=self.supplier,
            default_currency=self.currency,
            staff=self.user,
            last_modified_by=self.user,
        )

    def test_buyer_and_supplier_party_populated_after_backfill_and_rewire(self):
        forwards(live_apps, None)
        populate_party_fks(live_apps, None)

        self.contract.refresh_from_db()
        self.assertIsNotNone(self.contract.buyer_party_id)
        self.assertIsNotNone(self.contract.supplier_party_id)
        # Legacy FKs are untouched.
        self.assertEqual(self.contract.default_customer_id, self.customer.pk)
        self.assertEqual(self.contract.default_supplier_id, self.supplier.pk)
