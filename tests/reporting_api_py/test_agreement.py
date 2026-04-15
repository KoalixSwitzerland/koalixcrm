# -*- coding: utf-8 -*-
from django.test import LiveServerTestCase
from django.contrib.auth.models import User

from koalixcrm.reporting_api_py.reporting_api_client import KoalixCRMReportingAPIClient
from tests.factories.reporting.agreement_factory import StandardAgreementToTaskFactory
from tests.factories.reporting.task_factory import StandardTaskFactory
from tests.factories.reporting.resource_factory import StandardResourceFactory
from tests.factories.reporting.resource_price_factory import StandardResourcePriceFactory
from tests.factories.reporting.agreement_type_factory import StandardAgreementTypeFactory
from tests.factories.reporting.agreement_status_factory import AgreedAgreementStatusFactory
from tests.factories.settings.unit_factory import StandardUnitFactory


class AgreementAPITest(LiveServerTestCase):

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin', email='admin@example.com', password='adminpassword'
        )
        self.agreement = StandardAgreementToTaskFactory.create()
        self.api_client = KoalixCRMReportingAPIClient(
            self.live_server_url, username='admin', password='adminpassword'
        )

    def test_list(self):
        items = self.api_client.get_agreement_list()
        self.assertGreaterEqual(len(items), 1)

    def test_read(self):
        retrieved = self.api_client.get_agreement(self.agreement.id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.id, self.agreement.id)

    def test_write(self):
        task = StandardTaskFactory.create()
        resource = StandardResourceFactory.create()
        unit = StandardUnitFactory.create()
        costs = StandardResourcePriceFactory.create()
        agreement_type = StandardAgreementTypeFactory.create()
        agreement_status = AgreedAgreementStatusFactory.create()
        data = {
            "amount": "50.00",
            "date_from": "2024-01-01",
            "date_until": "2024-12-31",
            "task": {"id": task.id},
            "resource": {"id": resource.id},
            "unit": {"id": unit.id},
            "costs": {"id": costs.id},
            "type": {"id": agreement_type.id},
            "status": {"id": agreement_status.id},
        }
        created = self.api_client.create_agreement(data)
        self.assertIsNotNone(created)

    def test_modify(self):
        updated = self.api_client.update_agreement(
            self.agreement.id,
            {"amount": "200.00"}
        )
        self.assertIsNotNone(updated)
