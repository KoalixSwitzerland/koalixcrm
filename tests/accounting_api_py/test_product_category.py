# -*- coding: utf-8 -*-

from django.test import LiveServerTestCase
from django.contrib.auth.models import User

from koalixcrm.accounting_api_py.accounting_api_client import KoalixCRMAccountingAPIClient
from koalixcrm.accounting.factory.product_category_factory import StandardProductCategoryFactory
from koalixcrm.accounting.factory.account_factory import StandardAccountFactory
from koalixcrm.accounting.models import Account, ProductCategory


class ProductCategoryAPITest(LiveServerTestCase):
    """Test for the ProductCategory model API functionality."""

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword',
        )
        # ProductCategory requires FK to profit_account (type E) and loss_account (type S)
        self.profit_account = Account.objects.create(
            account_number=4000,
            title="Earnings Account",
            account_type="E",
            description="Test earnings account",
            is_open_reliabilities_account=False,
            is_open_interest_account=False,
            is_product_inventory_activa=False,
            is_a_customer_payment_account=False,
        )
        self.loss_account = Account.objects.create(
            account_number=5000,
            title="Spendings Account",
            account_type="S",
            description="Test spendings account",
            is_open_reliabilities_account=False,
            is_open_interest_account=False,
            is_product_inventory_activa=False,
            is_a_customer_payment_account=False,
        )
        self.product_category = ProductCategory.objects.create(
            title="Test Category",
            profit_account=self.profit_account,
            loss_account=self.loss_account,
        )
        self.api_client = KoalixCRMAccountingAPIClient(
            self.live_server_url,
            username='admin',
            password='adminpassword',
        )

    def test_list(self):
        items = self.api_client.get_product_category_list()
        self.assertGreaterEqual(len(items), 1)
        found = any(item.id == self.product_category.id for item in items)
        self.assertTrue(found, "Created ProductCategory not found in the list response")

    def test_read(self):
        retrieved = self.api_client.get_product_category(self.product_category.id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.id, self.product_category.id)

    def test_write(self):
        data = {
            "title": "New API Product Category",
            "profitAccount": {"id": self.profit_account.id},
            "lossAccount": {"id": self.loss_account.id},
        }
        created = self.api_client.create_product_category(data)
        self.assertIsNotNone(created)
        self.assertIsNotNone(created.id)

        db_obj = ProductCategory.objects.get(id=created.id)
        self.assertEqual(db_obj.title, "New API Product Category")

    def test_modify(self):
        updated = self.api_client.update_product_category(
            self.product_category.id, {"title": "Updated Category Title"}
        )
        self.assertIsNotNone(updated)
        self.assertEqual(updated.id, self.product_category.id)

        self.product_category.refresh_from_db()
        self.assertEqual(self.product_category.title, "Updated Category Title")
