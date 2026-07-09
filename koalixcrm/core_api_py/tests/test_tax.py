# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.test import LiveServerTestCase

from koalixcrm.core.models.tax import Tax
from koalixcrm.core_api_py.core_api_client import KoalixCRMCoreAPIClient
from koalixcrm.core.tests.factories.tax_factory import StandardTaxFactory


class TaxAPITest(LiveServerTestCase):
    """Test for the Tax model API functionality."""

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword',
        )
        self.tax = StandardTaxFactory.create()
        self.api_client = KoalixCRMCoreAPIClient(
            self.live_server_url,
            username='admin',
            password='adminpassword',
            workspace_id=1,
        )

    def test_list(self):
        items = self.api_client.get_tax_list()
        self.assertGreaterEqual(len(items), 1)
        found = any(item.id == self.tax.id for item in items)
        self.assertTrue(found, "Created Tax not found in the list response")

    def test_read(self):
        retrieved = self.api_client.get_tax(self.tax.id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.id, self.tax.id)

    def test_write(self):
        data = {
            "tax_rate": "8.00",
            "name": "New Test Tax",
        }
        created = self.api_client.create_tax(data)
        self.assertIsNotNone(created)
        self.assertIsNotNone(created.id)

        db_obj = Tax.objects.get(id=created.id)
        self.assertEqual(db_obj.name, "New Test Tax")

    def test_modify(self):
        updated = self.api_client.update_tax(
            self.tax.id, {"name": "Updated Tax Name"}
        )
        self.assertIsNotNone(updated)
        self.assertEqual(updated.id, self.tax.id)

        self.tax.refresh_from_db()
        self.assertEqual(self.tax.name, "Updated Tax Name")
