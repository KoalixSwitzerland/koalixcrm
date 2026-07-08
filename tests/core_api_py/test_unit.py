# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.test import LiveServerTestCase

from koalixcrm.core.models.unit import Unit
from koalixcrm.core_api_py.core_api_client import KoalixCRMCoreAPIClient
from koalixcrm.core.tests.factories.unit_factory import StandardUnitFactory


class UnitAPITest(LiveServerTestCase):
    """Test for the Unit model API functionality."""

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword',
        )
        self.unit = StandardUnitFactory.create()
        self.api_client = KoalixCRMCoreAPIClient(
            self.live_server_url,
            username='admin',
            password='adminpassword',
            workspace_id=1,
        )

    def test_list(self):
        items = self.api_client.get_unit_list()
        self.assertGreaterEqual(len(items), 1)
        found = any(item.id == self.unit.id for item in items)
        self.assertTrue(found, "Created Unit not found in the list response")

    def test_read(self):
        retrieved = self.api_client.get_unit(self.unit.id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.id, self.unit.id)

    def test_write(self):
        data = {
            "description": "Liter",
            "short_name": "l",
            "is_a_fraction_of": None,
        }
        created = self.api_client.create_unit(data)
        self.assertIsNotNone(created)
        self.assertIsNotNone(created.id)

        db_obj = Unit.objects.get(id=created.id)
        self.assertEqual(db_obj.description, "Liter")
        self.assertEqual(db_obj.short_name, "l")

    def test_modify(self):
        updated = self.api_client.update_unit(
            self.unit.id, {"description": "Updated Unit"}
        )
        self.assertIsNotNone(updated)
        self.assertEqual(updated.id, self.unit.id)

        self.unit.refresh_from_db()
        self.assertEqual(self.unit.description, "Updated Unit")
