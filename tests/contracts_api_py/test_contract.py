# -*- coding: utf-8 -*-

from django.test import LiveServerTestCase
from django.contrib.auth.models import User

from koalixcrm.contracts_api_py.contracts_api_client import KoalixCRMContractsAPIClient
from koalixcrm.contracts.factory.contract_factory import StandardContractFactory
from koalixcrm.crm.factory.customer_factory import StandardCustomerFactory
from koalixcrm.crm.factory.customer_billing_cycle_factory import StandardCustomerBillingCycleFactory
from koalixcrm.products.factory.currency_factory import StandardCurrencyFactory
from koalixcrm.contracts.models.contract import Contract


class ContractAPITest(LiveServerTestCase):
    """Test for the Contract model API functionality."""

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword',
        )
        self.billing_cycle = StandardCustomerBillingCycleFactory.create()
        self.customer = StandardCustomerFactory.create(
            default_customer_billing_cycle=self.billing_cycle,
        )
        self.currency = StandardCurrencyFactory.create()
        self.contract = StandardContractFactory.create(
            staff=self.admin_user,
            default_customer=self.customer,
            default_currency=self.currency,
            last_modified_by=self.admin_user,
        )
        self.api_client = KoalixCRMContractsAPIClient(
            self.live_server_url,
            username='admin',
            password='adminpassword',
        )

    def test_list(self):
        items = self.api_client.get_contract_list()
        self.assertGreaterEqual(len(items), 1)
        found = any(item.id == self.contract.id for item in items)
        self.assertTrue(found, "Created Contract not found in the list response")

    def test_read(self):
        retrieved = self.api_client.get_contract(self.contract.id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.id, self.contract.id)

    def test_write(self):
        data = {
            "description": "New API Contract",
            "staff": self.admin_user.id,
            "default_customer": self.customer.id,
            "default_currency": self.currency.id,
            "last_modified_by": self.admin_user.id,
        }
        created = self.api_client.create_contract(data)
        self.assertIsNotNone(created)
        self.assertIsNotNone(created.id)

        db_obj = Contract.objects.get(id=created.id)
        self.assertEqual(db_obj.description, "New API Contract")

    def test_modify(self):
        updated = self.api_client.update_contract(
            self.contract.id, {"description": "Updated Contract Description"}
        )
        self.assertIsNotNone(updated)
        self.assertEqual(updated.id, self.contract.id)

        self.contract.refresh_from_db()
        self.assertEqual(self.contract.description, "Updated Contract Description")
