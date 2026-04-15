# -*- coding: utf-8 -*-
from django.test import LiveServerTestCase
from django.contrib.auth.models import User

from koalixcrm.reporting_api_py.reporting_api_client import KoalixCRMReportingAPIClient
from tests.factories.reporting.agreement_status_factory import AgreedAgreementStatusFactory


class AgreementStatusAPITest(LiveServerTestCase):

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin', email='admin@example.com', password='adminpassword'
        )
        self.agreement_status = AgreedAgreementStatusFactory.create()
        self.api_client = KoalixCRMReportingAPIClient(
            self.live_server_url, username='admin', password='adminpassword'
        )

    def test_list(self):
        items = self.api_client.get_agreement_status_list()
        self.assertGreaterEqual(len(items), 1)

    def test_read(self):
        retrieved = self.api_client.get_agreement_status(self.agreement_status.id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.id, self.agreement_status.id)

    def test_write(self):
        data = {
            "title": "New Agreement Status",
            "description": "A new agreement status",
            "is_agreed": False,
        }
        created = self.api_client.create_agreement_status(data)
        self.assertIsNotNone(created)

    def test_modify(self):
        updated = self.api_client.update_agreement_status(
            self.agreement_status.id,
            {"description": "Updated agreement status description"}
        )
        self.assertIsNotNone(updated)
