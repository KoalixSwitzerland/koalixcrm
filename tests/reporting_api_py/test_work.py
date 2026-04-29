# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.test import LiveServerTestCase

from koalixcrm.reporting_api_py.reporting_api_client import KoalixCRMReportingAPIClient
from tests.factories.reporting.human_resource_factory import (
    StandardHumanResourceFactory,
)
from tests.factories.reporting.reporting_period_factory import (
    StandardReportingPeriodFactory,
)
from tests.factories.reporting.task_factory import StandardTaskFactory
from tests.factories.reporting.work_factory import StandardWorkFactory


class WorkAPITest(LiveServerTestCase):

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin', email='admin@example.com', password='adminpassword'
        )
        self.work = StandardWorkFactory.create()
        self.api_client = KoalixCRMReportingAPIClient(
            self.live_server_url, username='admin', password='adminpassword', workspace_id=1)

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
        human_resource = StandardHumanResourceFactory.create()
        data = {
            "human_resource": {"id": human_resource.id},
            "task": {"id": task.id},
            "reporting_period": {"id": reporting_period.id},
            "date": "2024-01-15",
            "start_time": None,
            "stop_time": None,
            "worked_hours": "2.00",
            "short_description": "API work entry",
            "description": "Created via API test",
        }
        created = self.api_client.create_work(data)
        self.assertIsNotNone(created)

    def test_modify(self):
        updated = self.api_client.update_work(
            self.work.id,
            {"short_description": "Updated work description"}
        )
        self.assertIsNotNone(updated)
