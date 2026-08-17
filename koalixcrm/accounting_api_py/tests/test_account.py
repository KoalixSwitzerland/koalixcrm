# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.test import LiveServerTestCase

from koalixcrm.accounting.models import Account
from koalixcrm.accounting_api_py.accounting_api_client import (
    KoalixCRMAccountingAPIClient,
)
from koalixcrm.accounting.tests.factories.account_factory import StandardAccountFactory
from koalixcrm.core.tests.factories.workspace_factory import DefaultWorkspaceFactory


class AccountAPITest(LiveServerTestCase):
    """Test for the Account model API functionality."""

    def setUp(self):
        self.workspace = DefaultWorkspaceFactory()
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword',
        )
        self.account = StandardAccountFactory.create()
        self.api_client = KoalixCRMAccountingAPIClient(
            self.live_server_url,
            username='admin',
            password='adminpassword',
            workspace_id=self.workspace.pk,
        )

    def test_list(self):
        items = self.api_client.get_account_list()
        self.assertGreaterEqual(len(items), 1)
        found = any(item.id == self.account.id for item in items)
        self.assertTrue(found, "Created Account not found in the list response")

    def test_read(self):
        retrieved = self.api_client.get_account(self.account.id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.id, self.account.id)

    def test_write(self):
        data = {
            "account_number": 3000,
            "title": "New API Account",
            "account_type": "A",
            "description": "Created via API test",
            "is_open_reliabilities_account": False,
            "is_open_interest_account": False,
            "is_product_inventory_activa": False,
            "is_a_customer_payment_account": False,
        }
        created = self.api_client.create_account(data)
        self.assertIsNotNone(created)
        self.assertIsNotNone(created.id)

        db_obj = Account.objects.get(id=created.id)
        self.assertEqual(db_obj.title, "New API Account")
        self.assertEqual(db_obj.account_number, 3000)

    def test_modify(self):
        updated = self.api_client.update_account(
            self.account.id, {"title": "Updated Account Title"}
        )
        self.assertIsNotNone(updated)
        self.assertEqual(updated.id, self.account.id)

        self.account.refresh_from_db()
        self.assertEqual(self.account.title, "Updated Account Title")
