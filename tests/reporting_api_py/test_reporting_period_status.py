# -*- coding: utf-8 -*-
from django.test import LiveServerTestCase
from django.contrib.auth.models import User

from koalixcrm.reporting_api_py.reporting_api_client import KoalixCRMReportingAPIClient
from tests.factories.reporting.reporting_period_status_factory import ReportingReportingPeriodStatusFactory


class ReportingPeriodStatusAPITest(LiveServerTestCase):

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin', email='admin@example.com', password='adminpassword'
        )
        self.reporting_period_status = ReportingReportingPeriodStatusFactory.create()
        self.api_client = KoalixCRMReportingAPIClient(
            self.live_server_url, username='admin', password='adminpassword', workspace_id=1)

    def test_list(self):
        items = self.api_client.get_reporting_period_status_list()
        self.assertGreaterEqual(len(items), 1)

    def test_read(self):
        retrieved = self.api_client.get_reporting_period_status(self.reporting_period_status.id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.id, self.reporting_period_status.id)

    def test_write(self):
        data = {
            "title": "New Reporting Period Status",
            "description": "A new reporting period status",
            "is_done": False,
        }
        created = self.api_client.create_reporting_period_status(data)
        self.assertIsNotNone(created)

    def test_modify(self):
        updated = self.api_client.update_reporting_period_status(
            self.reporting_period_status.id,
            {"description": "Updated reporting period status description"}
        )
        self.assertIsNotNone(updated)
