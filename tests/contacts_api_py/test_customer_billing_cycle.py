# -*- coding: utf-8 -*-

from django.test import LiveServerTestCase
from django.contrib.auth.models import User

from koalixcrm.contacts_api_py.contacts_api_client import KoalixCRMContactsAPIClient
from tests.factories.contacts.customer_billing_cycle_factory import StandardCustomerBillingCycleFactory
from koalixcrm.contacts.models import CustomerBillingCycle


class CustomerBillingCycleAPITest(LiveServerTestCase):
    """Test for the CustomerBillingCycle model API functionality."""

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword',
        )
        self.billing_cycle = StandardCustomerBillingCycleFactory.create(
            name="Test Billing Cycle",
        )
        self.api_client = KoalixCRMContactsAPIClient(
            self.live_server_url,
            username='admin',
            password='adminpassword',
            workspace_id=1,
        )

    def test_list(self):
        items = self.api_client.get_customer_billing_cycle_list()
        self.assertGreaterEqual(len(items), 1)
        found = any(item.id == self.billing_cycle.id for item in items)
        self.assertTrue(found, "Created CustomerBillingCycle not found in the list response")

    def test_read(self):
        retrieved = self.api_client.get_customer_billing_cycle(self.billing_cycle.id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.id, self.billing_cycle.id)

    def test_write(self):
        data = {
            "name": "New API Billing Cycle",
            "time_to_payment_date": 60,
            "payment_reminder_time_to_payment": 45,
        }
        created = self.api_client.create_customer_billing_cycle(data)
        self.assertIsNotNone(created)
        self.assertIsNotNone(created.id)

        db_obj = CustomerBillingCycle.objects.get(id=created.id)
        self.assertEqual(db_obj.name, "New API Billing Cycle")
        self.assertEqual(db_obj.time_to_payment_date, 60)

    def test_modify(self):
        updated = self.api_client.update_customer_billing_cycle(
            self.billing_cycle.id, {"name": "Updated Billing Cycle"}
        )
        self.assertIsNotNone(updated)
        self.assertEqual(updated.id, self.billing_cycle.id)

        self.billing_cycle.refresh_from_db()
        self.assertEqual(self.billing_cycle.name, "Updated Billing Cycle")
