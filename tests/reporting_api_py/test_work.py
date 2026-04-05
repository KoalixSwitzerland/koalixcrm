# -*- coding: utf-8 -*-
from django.test import LiveServerTestCase
from django.contrib.auth.models import User

from koalixcrm.reporting_api_py.reporting_api_client import KoalixCRMReportingAPIClient
from koalixcrm.reporting.factory.work_factory import StandardWorkFactory
from koalixcrm.reporting.factory.task_factory import StandardTaskFactory
from koalixcrm.reporting.factory.reporting_period_factory import StandardReportingPeriodFactory
from koalixcrm.djangoUserExtension.factories.factory_user_extension import StandardUserExtensionFactory


class WorkAPITest(LiveServerTestCase):

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin', email='admin@example.com', password='adminpassword'
        )
        self.work = StandardWorkFactory.create()
        self.api_client = KoalixCRMReportingAPIClient(
            self.live_server_url, username='admin', password='adminpassword'
        )

    def test_list(self):
        items = self.api_client.get_work_list()
        self.assertGreaterEqual(len(items), 1)

    def test_read(self):
        retrieved = self.api_client.get_work(self.work.id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.id, self.work.id)

    def test_write(self):
        task = StandardTaskFactory.create()
        reporting_period = StandardReportingPeriodFactory.create()
        human_resource = StandardUserExtensionFactory.create()
        data = {
            "humanResource": {"id": human_resource.id},
            "task": {"id": task.id},
            "reportingPeriod": {"id": reporting_period.id},
            "date": "2024-01-15",
            "startTime": None,
            "stopTime": None,
            "workedHours": "2.00",
            "shortDescription": "API work entry",
            "description": "Created via API test",
        }
        created = self.api_client.create_work(data)
        self.assertIsNotNone(created)

    def test_modify(self):
        updated = self.api_client.update_work(
            self.work.id,
            {"shortDescription": "Updated work description"}
        )
        self.assertIsNotNone(updated)
