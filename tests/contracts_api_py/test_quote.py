# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.test import LiveServerTestCase

from koalixcrm.contracts.models.quotation import Quotation
from koalixcrm.contracts_api_py.contracts_api_client import KoalixCRMContractsAPIClient
from koalixcrm.contacts.tests.factories.customer_billing_cycle_factory import (
    StandardCustomerBillingCycleFactory,
)
from koalixcrm.contacts.tests.factories.customer_factory import StandardCustomerFactory
from koalixcrm.contracts.tests.factories.contract_factory import StandardContractFactory
from koalixcrm.contracts.tests.factories.quotation_factory import StandardQuotationFactory
from koalixcrm.core.tests.factories.currency_factory import StandardCurrencyFactory


class QuotationAPITest(LiveServerTestCase):
    """Test for the Quotation model API functionality."""

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword',
        )
        self.billing_cycle = StandardCustomerBillingCycleFactory.create()
        self.customer = StandardCustomerFactory.create(
            default_billing_cycle=self.billing_cycle,
        )
        self.currency = StandardCurrencyFactory.create()
        self.contract = StandardContractFactory.create(
            staff=self.admin_user,
            buyer_party=self.customer,
            default_currency=self.currency,
            last_modified_by=self.admin_user,
        )
        self.quotation = StandardQuotationFactory.create(
            contract=self.contract,
            party=self.customer,
            currency=self.currency,
            staff=self.admin_user,
            last_modified_by=self.admin_user,
        )
        self.api_client = KoalixCRMContractsAPIClient(
            self.live_server_url,
            username='admin',
            password='adminpassword',
            workspace_id=1,
        )

    def test_list(self):
        items = self.api_client.get_quotation_list()
        self.assertGreaterEqual(len(items), 1)
        found = any(item.id == self.quotation.id for item in items)
        self.assertTrue(found, "Created Quotation not found in the list response")

    def test_read(self):
        retrieved = self.api_client.get_quotation(self.quotation.id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.id, self.quotation.id)

    def test_write(self):
        data = {
            "contract": self.contract.id,
            "party": self.customer.id,
            "currency": self.currency.id,
            "staff": self.admin_user.id,
            "last_modified_by": self.admin_user.id,
            "description": "New API Quotation",
            "discount": "0.00",
            "valid_until": "2026-06-01",
            "status": "I",
        }
        created = self.api_client.create_quotation(data)
        self.assertIsNotNone(created)
        self.assertIsNotNone(created.id)

        db_obj = Quotation.objects.get(id=created.id)
        self.assertEqual(db_obj.description, "New API Quotation")
        self.assertEqual(db_obj.status, "I")

    def test_modify(self):
        updated = self.api_client.update_quotation(
            self.quotation.id, {"description": "Updated Quotation Description"}
        )
        self.assertIsNotNone(updated)
        self.assertEqual(updated.id, self.quotation.id)

        self.quotation.refresh_from_db()
        self.assertEqual(self.quotation.description, "Updated Quotation Description")
