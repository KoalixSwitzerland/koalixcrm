# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.test import LiveServerTestCase

from koalixcrm.core.models.currency import Currency
from koalixcrm.core_api_py.core_api_client import KoalixCRMCoreAPIClient
from tests.factories.core.currency_factory import StandardCurrencyFactory


class CurrencyAPITest(LiveServerTestCase):
    """Test for the Currency model API functionality."""

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword',
        )
        self.currency = StandardCurrencyFactory.create()
        self.api_client = KoalixCRMCoreAPIClient(
            self.live_server_url,
            username='admin',
            password='adminpassword',
            workspace_id=1,
        )

    def test_list(self):
        items = self.api_client.get_currency_list()
        self.assertGreaterEqual(len(items), 1)
        found = any(item.id == self.currency.id for item in items)
        self.assertTrue(found, "Created Currency not found in the list response")

    def test_read(self):
        retrieved = self.api_client.get_currency(self.currency.id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.id, self.currency.id)

    def test_write(self):
        data = {
            "description": "US Dollar",
            "short_name": "USD",
            "rounding": "0.01",
        }
        created = self.api_client.create_currency(data)
        self.assertIsNotNone(created)
        self.assertIsNotNone(created.id)

        db_obj = Currency.objects.get(id=created.id)
        self.assertEqual(db_obj.description, "US Dollar")
        self.assertEqual(db_obj.short_name, "USD")

    def test_modify(self):
        updated = self.api_client.update_currency(
            self.currency.id, {"description": "Updated Currency"}
        )
        self.assertIsNotNone(updated)
        self.assertEqual(updated.id, self.currency.id)

        self.currency.refresh_from_db()
        self.assertEqual(self.currency.description, "Updated Currency")
