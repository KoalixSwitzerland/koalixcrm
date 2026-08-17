# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.test import LiveServerTestCase

from koalixcrm.reporting_api_py.reporting_api_client import KoalixCRMReportingAPIClient
from koalixcrm.reporting.tests.factories.task_status_factory import StartedTaskStatusFactory
from koalixcrm.core.tests.factories.workspace_factory import DefaultWorkspaceFactory


class TaskStatusAPITest(LiveServerTestCase):

    def setUp(self):
        self.workspace = DefaultWorkspaceFactory()
        self.admin_user = User.objects.create_superuser(
            username='admin', email='admin@example.com', password='adminpassword'
        )
        self.task_status = StartedTaskStatusFactory.create()
        self.api_client = KoalixCRMReportingAPIClient(
            self.live_server_url, username='admin', password='adminpassword', workspace_id=self.workspace.pk)

    def test_list(self):
        items = self.api_client.get_task_status_list()
        self.assertGreaterEqual(len(items), 1)

    def test_read(self):
        retrieved = self.api_client.get_task_status(self.task_status.id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.id, self.task_status.id)

    def test_write(self):
        data = {
            "title": "New Task Status",
            "description": "A new task status",
            "is_done": False,
        }
        created = self.api_client.create_task_status(data)
        self.assertIsNotNone(created)

    def test_modify(self):
        updated = self.api_client.update_task_status(
            self.task_status.id,
            {"description": "Updated task status description"}
        )
        self.assertIsNotNone(updated)
