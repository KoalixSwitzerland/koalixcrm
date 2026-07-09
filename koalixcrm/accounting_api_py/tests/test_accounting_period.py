# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.test import LiveServerTestCase

from koalixcrm.accounting.models import AccountingPeriod
from koalixcrm.accounting_api_py.accounting_api_client import (
    KoalixCRMAccountingAPIClient,
)
from koalixcrm.accounting.tests.factories.accounting_period_factory import (
    StandardAccountingPeriodFactory,
)


class AccountingPeriodAPITest(LiveServerTestCase):
    """Test for the AccountingPeriod model API functionality."""

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword',
        )
        self.accounting_period = StandardAccountingPeriodFactory.create()
        self.api_client = KoalixCRMAccountingAPIClient(
            self.live_server_url,
            username='admin',
            password='adminpassword',
            workspace_id=1,
        )

    def test_list(self):
        items = self.api_client.get_accounting_period_list()
        self.assertGreaterEqual(len(items), 1)
        found = any(item.id == self.accounting_period.id for item in items)
        self.assertTrue(found, "Created AccountingPeriod not found in the list response")

    def test_read(self):
        retrieved = self.api_client.get_accounting_period(self.accounting_period.id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.id, self.accounting_period.id)

    def test_write(self):
        data = {
            "title": "Fiscal Year 2025",
            "begin": "2025-01-01",
            "end": "2025-12-31",
        }
        created = self.api_client.create_accounting_period(data)
        self.assertIsNotNone(created)
        self.assertIsNotNone(created.id)

        db_obj = AccountingPeriod.objects.get(id=created.id)
        self.assertEqual(db_obj.title, "Fiscal Year 2025")

    def test_modify(self):
        updated = self.api_client.update_accounting_period(
            self.accounting_period.id, {"title": "Updated Period Title"}
        )
        self.assertIsNotNone(updated)
        self.assertEqual(updated.id, self.accounting_period.id)

        self.accounting_period.refresh_from_db()
        self.assertEqual(self.accounting_period.title, "Updated Period Title")
