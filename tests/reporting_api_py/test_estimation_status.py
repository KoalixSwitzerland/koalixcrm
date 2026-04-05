# -*- coding: utf-8 -*-
from django.test import LiveServerTestCase
from django.contrib.auth.models import User

from koalixcrm.reporting_api_py.reporting_api_client import KoalixCRMReportingAPIClient
from koalixcrm.reporting.factory.estimation_status_factory import StartedEstimationStatusFactory


class EstimationStatusAPITest(LiveServerTestCase):

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin', email='admin@example.com', password='adminpassword'
        )
        self.estimation_status = StartedEstimationStatusFactory.create()
        self.api_client = KoalixCRMReportingAPIClient(
            self.live_server_url, username='admin', password='adminpassword'
        )

    def test_list(self):
        items = self.api_client.get_estimation_status_list()
        self.assertGreaterEqual(len(items), 1)

    def test_read(self):
        retrieved = self.api_client.get_estimation_status(self.estimation_status.id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.id, self.estimation_status.id)

    def test_write(self):
        data = {
            "title": "New Estimation Status",
            "description": "A new estimation status",
            "isObsolete": False,
        }
        created = self.api_client.create_estimation_status(data)
        self.assertIsNotNone(created)

    def test_modify(self):
        updated = self.api_client.update_estimation_status(
            self.estimation_status.id,
            {"description": "Updated estimation status description"}
        )
        self.assertIsNotNone(updated)
