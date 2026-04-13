# -*- coding: utf-8 -*-

from django.test import LiveServerTestCase
from django.contrib.auth.models import User

from koalixcrm.crm_api_py.crm_api_client import KoalixCRMContactsAPIClient
from koalixcrm.crm.factory.customer_factory import StandardCustomerFactory
from koalixcrm.crm.factory.customer_billing_cycle_factory import StandardCustomerBillingCycleFactory
from koalixcrm.crm.models import Customer


class CustomerAPITest(LiveServerTestCase):
    """Test for the Customer model API functionality."""

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword',
        )
        self.billing_cycle = StandardCustomerBillingCycleFactory.create()
        self.customer = StandardCustomerFactory.create(
            name="Test Customer",
            default_customer_billing_cycle=self.billing_cycle,
        )
        self.api_client = KoalixCRMContactsAPIClient(
            self.live_server_url,
            username='admin',
            password='adminpassword',
        )

    def test_list(self):
        items = self.api_client.get_customer_list()
        self.assertGreaterEqual(len(items), 1)
        found = any(item.id == self.customer.id for item in items)
        self.assertTrue(found, "Created Customer not found in the list response")

    def test_read(self):
        retrieved = self.api_client.get_customer(self.customer.id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.id, self.customer.id)

    def test_write(self):
        data = {
            "name": "New API Customer",
            "default_customer_billing_cycle": {"id": self.billing_cycle.id},
            "is_member_of": [],
            "is_lead": False,
        }
        created = self.api_client.create_customer(data)
        self.assertIsNotNone(created)
        self.assertIsNotNone(created.id)

        db_obj = Customer.objects.get(id=created.id)
        self.assertEqual(db_obj.name, "New API Customer")

    def test_modify(self):
        updated = self.api_client.update_customer(
            self.customer.id, {"name": "Updated Customer Name"}
        )
        self.assertIsNotNone(updated)
        self.assertEqual(updated.id, self.customer.id)

        self.customer.refresh_from_db()
        self.assertEqual(self.customer.name, "Updated Customer Name")
