# -*- coding: utf-8 -*-
from django.test import LiveServerTestCase
from django.contrib.auth.models import User

from koalixcrm.reporting_api_py.reporting_api_client import KoalixCRMReportingAPIClient
from tests.factories.reporting.human_resource_factory import StandardHumanResourceFactory
from tests.factories.djangoUserExtension.factory_user_extension import StandardUserExtensionFactory
from tests.factories.reporting.resource_type_factory import StandardResourceTypeFactory
from tests.factories.reporting.resource_manager_factory import StandardResourceManagerFactory


class HumanResourceAPITest(LiveServerTestCase):

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin', email='admin@example.com', password='adminpassword'
        )
        self.human_resource = StandardHumanResourceFactory.create()
        self.api_client = KoalixCRMReportingAPIClient(
            self.live_server_url, username='admin', password='adminpassword', workspace_id=1)

    def test_list(self):
        items = self.api_client.get_human_resource_list()
        self.assertGreaterEqual(len(items), 1)

    def test_read(self):
        retrieved = self.api_client.get_human_resource(self.human_resource.id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.id, self.human_resource.id)

    def test_write(self):
        user_extension = StandardUserExtensionFactory.create()
        resource_type = StandardResourceTypeFactory.create()
        resource_manager = StandardResourceManagerFactory.create()
        data = {
            "user": {"id": user_extension.id},
            "resource_type": {"id": resource_type.id},
            "resource_manager": {"id": resource_manager.id},
        }
        created = self.api_client.create_human_resource(data)
        self.assertIsNotNone(created)

    def test_modify(self):
        new_resource_type = StandardResourceTypeFactory.create()
        updated = self.api_client.update_human_resource(
            self.human_resource.id,
            {"resource_type": {"id": new_resource_type.id}}
        )
        self.assertIsNotNone(updated)
