# -*- coding: utf-8 -*-
from django.test import LiveServerTestCase
from django.contrib.auth.models import User

from koalixcrm.reporting_api_py.reporting_api_client import KoalixCRMReportingAPIClient
from tests.factories.reporting.reporting_period_factory import StandardReportingPeriodFactory
from tests.factories.reporting.project_factory import StandardProjectFactory
from tests.factories.reporting.reporting_period_status_factory import ReportingReportingPeriodStatusFactory


class ReportingPeriodAPITest(LiveServerTestCase):

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin', email='admin@example.com', password='adminpassword'
        )
        self.reporting_period = StandardReportingPeriodFactory.create()
        self.api_client = KoalixCRMReportingAPIClient(
            self.live_server_url, username='admin', password='adminpassword'
        )

    def test_list(self):
        items = self.api_client.get_reporting_period_list()
        self.assertGreaterEqual(len(items), 1)

    def test_read(self):
        retrieved = self.api_client.get_reporting_period(self.reporting_period.id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.id, self.reporting_period.id)

    def test_write(self):
        project = StandardProjectFactory.create()
        status = ReportingReportingPeriodStatusFactory.create()
        data = {
            "title": "API Reporting Period",
            "begin": "2024-01-01",
            "end": "2024-06-30",
            "project": {"id": project.id},
            "status": {"id": status.id},
        }
        created = self.api_client.create_reporting_period(data)
        self.assertIsNotNone(created)

    def test_modify(self):
        updated = self.api_client.update_reporting_period(
            self.reporting_period.id,
            {"title": "Updated Reporting Period Title"}
        )
        self.assertIsNotNone(updated)
