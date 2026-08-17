# -*- coding: utf-8 -*-
"""Tests for the FOP-report-oriented custom actions on the accounting API:

- ``GET /accounts/<id>/booking-sums/?accounting_period=<id>``
- ``GET /accounting-periods/<id>/report-data/``

These are the endpoints the Java pdf-export-service will call to build
balancesheet and profit/loss statement XML without re-implementing the
booking arithmetic.
"""

import datetime
from decimal import Decimal

import requests
from django.contrib.auth.models import User
from django.test import LiveServerTestCase

from koalixcrm.accounting.models import Account, AccountingPeriod, Booking
from koalixcrm.core.tests.factories.workspace_factory import DefaultWorkspaceFactory
from koalixcrm.global_support_functions import make_date_utc

# REQ-0028: the `<workspace_id>` segment is authorized, so it has to name a
# real active workspace rather than a hard-coded `1`.
API_BASE_TEMPLATE = '/koalixcrm_accounting/api/v1/{workspace_id}'


class _AccountingFixture:
    """Creates a minimal but realistic fixture: two periods (prior + current),
    one asset account, one earnings account, and bookings spread across both
    periods so every aggregate has a non-trivial value to check.
    """

    def build(self):
        self.staff = User.objects.create_user(
            username='staff', password='x', is_staff=True
        )
        self.prior = AccountingPeriod.objects.create(
            title='FY 2017', begin='2017-01-01', end='2017-12-31',
        )
        self.current = AccountingPeriod.objects.create(
            title='FY 2018', begin='2018-01-01', end='2018-12-31',
        )
        self.asset = Account.objects.create(
            account_number=1000, title='Cash', account_type='A',
            is_open_reliabilities_account=False, is_open_interest_account=False,
            is_product_inventory_activa=False, is_a_customer_payment_account=False,
        )
        self.earnings = Account.objects.create(
            account_number=4000, title='Sales', account_type='E',
            is_open_reliabilities_account=False, is_open_interest_account=False,
            is_product_inventory_activa=False, is_a_customer_payment_account=False,
        )
        # Prior period: 100 flows earnings -> asset
        self._booking(self.earnings, self.asset, '100.00',
                      datetime.datetime(2017, 6, 1), self.prior)
        # Current period: another 250 flows earnings -> asset
        self._booking(self.earnings, self.asset, '250.00',
                      datetime.datetime(2018, 6, 1), self.current)

    def _booking(self, from_acc, to_acc, amount, when, period):
        Booking.objects.create(
            from_account=from_acc, to_account=to_acc, amount=amount,
            description='t', booking_date=make_date_utc(when),
            accounting_period=period, staff=self.staff,
            last_modified_by=self.staff,
        )


class BookingSumsAPITest(LiveServerTestCase):

    def setUp(self):
        User.objects.create_superuser('admin', 'a@b.c', 'adminpassword')
        self.workspace = DefaultWorkspaceFactory()
        self.api_base = API_BASE_TEMPLATE.format(workspace_id=self.workspace.pk)
        self.fx = _AccountingFixture()
        self.fx.build()
        self.auth = ('admin', 'adminpassword')

    def _get(self, path):
        r = requests.get(self.live_server_url + path, auth=self.auth)
        r.raise_for_status()
        return r.json()

    def test_account_booking_sums_requires_period(self):
        url = self.live_server_url + f'{self.api_base}/accounts/{self.fx.asset.id}/booking-sums/'
        r = requests.get(url, auth=self.auth)
        self.assertEqual(r.status_code, 400)

    def test_account_booking_sums_unknown_period_is_404(self):
        r = requests.get(
            self.live_server_url +
            f'{self.api_base}/accounts/{self.fx.asset.id}/booking-sums/?accounting_period=99999',
            auth=self.auth,
        )
        self.assertEqual(r.status_code, 404)

    def test_account_booking_sums_asset(self):
        data = self._get(
            f'{self.api_base}/accounts/{self.fx.asset.id}/booking-sums/'
            f'?accounting_period={self.fx.current.id}'
        )
        self.assertEqual(data['id'], self.fx.asset.id)
        self.assertEqual(data['account_type'], 'A')
        # Asset receives: 100 in prior, 250 in current, 350 total.
        self.assertEqual(Decimal(data['sum_within_accounting_period']), Decimal('250'))
        self.assertEqual(Decimal(data['sum_before_accounting_period']), Decimal('100'))
        self.assertEqual(Decimal(data['sum_through_now']), Decimal('350'))
        self.assertEqual(Decimal(data['sum_total']), Decimal('350'))

    def test_account_booking_sums_earnings_sign_flip(self):
        """Earnings/liability accounts flip sign — verify that behaviour leaks
        through the API so the Java side gets the same numbers as the legacy
        in-Django report."""
        data = self._get(
            f'{self.api_base}/accounts/{self.fx.earnings.id}/booking-sums/'
            f'?accounting_period={self.fx.current.id}'
        )
        self.assertEqual(data['account_type'], 'E')
        self.assertEqual(Decimal(data['sum_within_accounting_period']), Decimal('250'))
        self.assertEqual(Decimal(data['sum_before_accounting_period']), Decimal('100'))
        self.assertEqual(Decimal(data['sum_through_now']), Decimal('350'))
        self.assertEqual(Decimal(data['sum_total']), Decimal('350'))

    def test_accounting_period_report_data(self):
        data = self._get(
            f'{self.api_base}/accounting-periods/{self.fx.current.id}/report-data/'
        )
        self.assertEqual(data['id'], self.fx.current.id)
        # The two template FKs are exposed so the Java service can tell
        # whether it's rendering the balance sheet or the profit/loss report.
        self.assertIn('template_set_balance_sheet', data)
        self.assertIn('template_profit_loss_statement', data)
        self.assertEqual(Decimal(data['overall_earnings']), Decimal('250'))
        self.assertEqual(Decimal(data['overall_assets']), Decimal('350'))
        account_ids = {a['id'] for a in data['accounts']}
        self.assertEqual(account_ids, {self.fx.asset.id, self.fx.earnings.id})
        # Every account carries the four period-scoped sums.
        for a in data['accounts']:
            for k in ('sum_within_accounting_period', 'sum_through_now',
                      'sum_before_accounting_period', 'sum_total'):
                self.assertIn(k, a)
