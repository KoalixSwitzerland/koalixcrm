# -*- coding: utf-8 -*-
from django.test import LiveServerTestCase
from django.contrib.auth.models import User

from koalixcrm.reporting_api_py.reporting_api_client import KoalixCRMReportingAPIClient
from tests.factories.reporting.estimation_factory import StandardEstimationToTaskFactory
from tests.factories.reporting.task_factory import StandardTaskFactory
from tests.factories.reporting.resource_factory import StandardResourceFactory
from tests.factories.reporting.estimation_status_factory import StartedEstimationStatusFactory
from tests.factories.reporting.reporting_period_factory import StandardReportingPeriodFactory


class EstimationAPITest(LiveServerTestCase):

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin', email='admin@example.com', password='adminpassword'
        )
        self.estimation = StandardEstimationToTaskFactory.create()
        self.api_client = KoalixCRMReportingAPIClient(
            self.live_server_url, username='admin', password='adminpassword'
        )

    def test_list(self):
        items = self.api_client.get_estimation_list()
        self.assertGreaterEqual(len(items), 1)

    def test_read(self):
        retrieved = self.api_client.get_estimation(self.estimation.id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.id, self.estimation.id)

    def test_write(self):
        task = StandardTaskFactory.create()
        resource = StandardResourceFactory.create()
        status = StartedEstimationStatusFactory.create()
        reporting_period = StandardReportingPeriodFactory.create()
        data = {
            "amount": "75.00",
            "date_from": "2024-01-01",
            "date_until": "2024-06-30",
            "task": {"id": task.id},
            "resource": {"id": resource.id},
            "status": {"id": status.id},
            "reporting_period": reporting_period.id,
        }
        created = self.api_client.create_estimation(data)
        self.assertIsNotNone(created)

    def test_modify(self):
        updated = self.api_client.update_estimation(
            self.estimation.id,
            {"amount": "150.00"}
        )
        self.assertIsNotNone(updated)
