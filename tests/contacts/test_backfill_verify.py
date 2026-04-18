# -*- coding: utf-8 -*-
"""Tests for the pre-cutover verifier (issue #395 G2).

The verifier runs every backfill + FK-rewire invariant and raises
`BackfillVerificationError` on any mismatch. Tests here exercise the
two happy paths (fresh DB, DB with clean backfill) and one failure
path (drift in a FK-rewire check).
"""
from django.apps import apps as live_apps
from django.contrib.auth.models import User
from django.test import TestCase

from koalixcrm.contacts.backfill import forwards
from koalixcrm.contacts.backfill_verify import (
    BackfillVerificationError,
    verify_ready_for_cutover,
)
from koalixcrm.contacts.models.customer import Customer as LegacyCustomer
from koalixcrm.contacts.models.customer_billing_cycle import CustomerBillingCycle
from koalixcrm.contracts.models.contract import Contract
from koalixcrm.contracts.party_fk_rewire import populate_party_fks
from koalixcrm.core.models.currency import Currency


class VerifyOnEmptyDBTest(TestCase):
    def test_fresh_db_every_check_passes(self):
        checks = verify_ready_for_cutover(live_apps, raise_on_failure=False)
        for c in checks:
            self.assertTrue(
                c.passed,
                f"Check '{c.name}' failed on empty DB: "
                f"legacy={c.legacy_count} new={c.new_count}",
            )


class VerifyAfterCleanBackfillTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='migrationuser', is_staff=True)
        self.billing_cycle = CustomerBillingCycle.objects.create(
            name='Default', time_to_payment_date=30,
            payment_reminder_time_to_payment=14,
        )
        self.currency = Currency.objects.create(
            description='CHF', short_name='CHF', rounding='0.05',
        )
        self.customer = LegacyCustomer.objects.create(
            name='ACME AG', last_modified_by=self.user,
            default_customer_billing_cycle=self.billing_cycle,
            is_lead=False,
        )
        self.contract = Contract.objects.create(
            description='Test contract',
            default_customer=self.customer,
            default_currency=self.currency,
            staff=self.user,
            last_modified_by=self.user,
        )

    def test_verify_passes_after_backfill_and_fk_rewire(self):
        forwards(live_apps, None)
        populate_party_fks(live_apps, None)

        checks = verify_ready_for_cutover(live_apps, raise_on_failure=True)
        for c in checks:
            self.assertTrue(
                c.passed,
                f"Check '{c.name}' failed: "
                f"legacy={c.legacy_count} new={c.new_count}",
            )

    def test_verify_raises_when_fk_rewire_skipped(self):
        # Backfill ran, but the FK rewire didn't. Contract.buyer_party is
        # still null; the Contract-level invariant must fail.
        forwards(live_apps, None)

        with self.assertRaises(BackfillVerificationError) as ctx:
            verify_ready_for_cutover(live_apps, raise_on_failure=True)

        failed_names = [c.name for c in ctx.exception.failed_checks]
        self.assertTrue(
            any('buyer_party' in name for name in failed_names),
            f"Expected a buyer_party check in failures; got {failed_names}",
        )

        msg = str(ctx.exception)
        self.assertIn('Pre-cutover verification failed', msg)
        self.assertIn('hint:', msg)
        self.assertIn('docs/migration-v1.14.0-to-v2.0.0.md', msg)
