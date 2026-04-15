# -*- coding: utf-8 -*-
from django.test import LiveServerTestCase
from django.contrib.auth.models import User

from koalixcrm.reporting_api_py.reporting_api_client import KoalixCRMReportingAPIClient
from tests.factories.reporting.project_factory import StandardProjectFactory
from tests.factories.reporting.project_status_factory import StartedProjectStatusFactory
from tests.factories.settings.currency_factory import StandardCurrencyFactory
from tests.factories.djangoUserExtension.factory_template_set import StandardTemplateSetFactory


class ProjectAPITest(LiveServerTestCase):

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin', email='admin@example.com', password='adminpassword'
        )
        self.project = StandardProjectFactory.create()
        self.api_client = KoalixCRMReportingAPIClient(
            self.live_server_url, username='admin', password='adminpassword'
        )

    def test_list(self):
        items = self.api_client.get_project_list()
        self.assertGreaterEqual(len(items), 1)

    def test_read(self):
        retrieved = self.api_client.get_project(self.project.id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.id, self.project.id)

    def test_write(self):
        project_status = StartedProjectStatusFactory.create()
        default_currency = StandardCurrencyFactory.create()
        default_template_set = StandardTemplateSetFactory.create()
        data = {
            "project_name": "API Created Project",
            "description": "Created via API test",
            "project_status": {"id": project_status.id},
            "default_currency": {"id": default_currency.id},
            "default_template_set": {"id": default_template_set.id},
        }
        created = self.api_client.create_project(data)
        self.assertIsNotNone(created)

    def test_modify(self):
        updated = self.api_client.update_project(
            self.project.id,
            {"description": "Updated description via API"}
        )
        self.assertIsNotNone(updated)
