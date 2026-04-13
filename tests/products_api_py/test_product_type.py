# -*- coding: utf-8 -*-

from django.test import LiveServerTestCase
from django.contrib.auth.models import User

from koalixcrm.products_api_py.products_api_client import KoalixCRMProductsAPIClient
from koalixcrm.products.factory.product_type_factory import StandardProductTypeFactory
from koalixcrm.products.factory.unit_factory import StandardUnitFactory
from koalixcrm.products.factory.tax_factory import StandardTaxFactory
from koalixcrm.products.models.product_type import ProductType


class ProductTypeAPITest(LiveServerTestCase):
    """Test for the ProductType model API functionality."""

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword',
        )
        self.unit = StandardUnitFactory.create()
        self.tax = StandardTaxFactory.create()
        self.product_type = StandardProductTypeFactory.create(
            default_unit=self.unit,
            tax=self.tax,
            last_modified_by=self.admin_user,
        )
        self.api_client = KoalixCRMProductsAPIClient(
            self.live_server_url,
            username='admin',
            password='adminpassword',
        )

    def test_list(self):
        items = self.api_client.get_product_type_list()
        self.assertGreaterEqual(len(items), 1)
        found = any(item.id == self.product_type.id for item in items)
        self.assertTrue(found, "Created ProductType not found in the list response")

    def test_read(self):
        retrieved = self.api_client.get_product_type(self.product_type.id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.id, self.product_type.id)

    def test_write(self):
        from koalixcrm.accounting.models import ProductCategory, Account
        profit_account = Account.objects.create(
            account_number=4100, title="Profit", account_type="E",
            is_open_reliabilities_account=False, is_open_interest_account=False,
            is_product_inventory_activa=False, is_a_customer_payment_account=False,
        )
        loss_account = Account.objects.create(
            account_number=5100, title="Loss", account_type="S",
            is_open_reliabilities_account=False, is_open_interest_account=False,
            is_product_inventory_activa=False, is_a_customer_payment_account=False,
        )
        category = ProductCategory.objects.create(
            title="Test Cat", profit_account=profit_account, loss_account=loss_account,
        )
        data = {
            "title": "New API Product Type",
            "product_type_identifier": "API-001",
            "default_unit": {"id": self.unit.id},
            "tax": {"id": self.tax.id},
            "accounting_product_category": {"id": category.id},
        }
        created = self.api_client.create_product_type(data)
        self.assertIsNotNone(created)
        self.assertIsNotNone(created.id)

        db_obj = ProductType.objects.get(id=created.id)
        self.assertEqual(db_obj.title, "New API Product Type")

    def test_modify(self):
        updated = self.api_client.update_product_type(
            self.product_type.id, {"title": "Updated Product Type Title"}
        )
        self.assertIsNotNone(updated)
        self.assertEqual(updated.id, self.product_type.id)

        self.product_type.refresh_from_db()
        self.assertEqual(self.product_type.title, "Updated Product Type Title")
