# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.test import LiveServerTestCase

from koalixcrm.reporting_api_py.reporting_api_client import KoalixCRMReportingAPIClient
from tests.factories.reporting.project_factory import StandardProjectFactory
from tests.factories.reporting.task_factory import StandardTaskFactory
from tests.factories.reporting.task_status_factory import StartedTaskStatusFactory


class TaskAPITest(LiveServerTestCase):

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin', email='admin@example.com', password='adminpassword'
        )
        self.task = StandardTaskFactory.create()
        self.api_client = KoalixCRMReportingAPIClient(
            self.live_server_url, username='admin', password='adminpassword', workspace_id=1)

    def test_list(self):
        items = self.api_client.get_task_list()
        self.assertGreaterEqual(len(items), 1)

    def test_read(self):
        retrieved = self.api_client.get_task(self.task.id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.id, self.task.id)

    def test_write(self):
        project = StandardProjectFactory.create()
        task_status = StartedTaskStatusFactory.create()
        data = {
            "title": "API Created Task",
            "description": "Created via API test",
            "project": {"id": project.id},
            "status": {"id": task_status.id},
            "last_status_change": "2024-01-15",
        }
        created = self.api_client.create_task(data)
        self.assertIsNotNone(created)

    def test_modify(self):
        updated = self.api_client.update_task(
            self.task.id,
            {"description": "Updated task description"}
        )
        self.assertIsNotNone(updated)
