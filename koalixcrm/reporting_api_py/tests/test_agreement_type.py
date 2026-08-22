# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.test import LiveServerTestCase

from koalixcrm.reporting_api_py.reporting_api_client import KoalixCRMReportingAPIClient
from koalixcrm.reporting.tests.factories.agreement_type_factory import (
    StandardAgreementTypeFactory,
)
from koalixcrm.core.tests.factories.workspace_factory import DefaultWorkspaceFactory


class AgreementTypeAPITest(LiveServerTestCase):

    def setUp(self):
        self.workspace = DefaultWorkspaceFactory()
        self.admin_user = User.objects.create_superuser(
            username='admin', email='admin@example.com', password='adminpassword'
        )
        self.agreement_type = StandardAgreementTypeFactory.create()
        self.api_client = KoalixCRMReportingAPIClient(
            self.live_server_url, username='admin', password='adminpassword', workspace_id=self.workspace.pk)

    def test_list(self):
        items = self.api_client.get_agreement_type_list()
        self.assertGreaterEqual(len(items), 1)

    def test_read(self):
        retrieved = self.api_client.get_agreement_type(self.agreement_type.id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.id, self.agreement_type.id)

    def test_write(self):
        data = {
            "title": "New Agreement Type",
            "description": "A new agreement type",
        }
        created = self.api_client.create_agreement_type(data)
        self.assertIsNotNone(created)

    def test_modify(self):
        updated = self.api_client.update_agreement_type(
            self.agreement_type.id,
            {"description": "Updated agreement type description"}
        )
        self.assertIsNotNone(updated)
