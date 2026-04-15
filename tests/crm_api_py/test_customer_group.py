# -*- coding: utf-8 -*-

from django.test import LiveServerTestCase
from django.contrib.auth.models import User

from koalixcrm.crm_api_py.crm_api_client import KoalixCRMContactsAPIClient
from tests.factories.crm.customer_group_factory import StandardCustomerGroupFactory
from koalixcrm.crm.models import CustomerGroup


class CustomerGroupAPITest(LiveServerTestCase):
    """Test for the CustomerGroup model API functionality."""

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword',
        )
        self.customer_group = StandardCustomerGroupFactory.create(
            name="Test Customer Group",
        )
        self.api_client = KoalixCRMContactsAPIClient(
            self.live_server_url,
            username='admin',
            password='adminpassword',
        )

    def test_list(self):
        items = self.api_client.get_customer_group_list()
        self.assertGreaterEqual(len(items), 1)
        found = any(item.id == self.customer_group.id for item in items)
        self.assertTrue(found, "Created CustomerGroup not found in the list response")

    def test_read(self):
        retrieved = self.api_client.get_customer_group(self.customer_group.id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.id, self.customer_group.id)

    def test_write(self):
        data = {
            "name": "New API Customer Group",
        }
        created = self.api_client.create_customer_group(data)
        self.assertIsNotNone(created)
        self.assertIsNotNone(created.id)

        db_obj = CustomerGroup.objects.get(id=created.id)
        self.assertEqual(db_obj.name, "New API Customer Group")

    def test_modify(self):
        updated = self.api_client.update_customer_group(
            self.customer_group.id, {"name": "Updated Group Name"}
        )
        self.assertIsNotNone(updated)
        self.assertEqual(updated.id, self.customer_group.id)

        self.customer_group.refresh_from_db()
        self.assertEqual(self.customer_group.name, "Updated Group Name")
