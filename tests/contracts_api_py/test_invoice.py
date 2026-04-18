# -*- coding: utf-8 -*-

from django.test import LiveServerTestCase
from django.contrib.auth.models import User

from koalixcrm.contracts_api_py.contracts_api_client import KoalixCRMContractsAPIClient
from tests.factories.contracts.invoice_factory import StandardInvoiceFactory
from tests.factories.contracts.contract_factory import StandardContractFactory
from tests.factories.contacts.customer_factory import StandardCustomerFactory
from tests.factories.contacts.customer_billing_cycle_factory import StandardCustomerBillingCycleFactory
from tests.factories.core.currency_factory import StandardCurrencyFactory
from koalixcrm.contracts.models.invoice import Invoice


class InvoiceAPITest(LiveServerTestCase):
    """Test for the Invoice model API functionality."""

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
        self.invoice = StandardInvoiceFactory.create(
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
        )

    def test_list(self):
        items = self.api_client.get_invoice_list()
        self.assertGreaterEqual(len(items), 1)
        found = any(item.id == self.invoice.id for item in items)
        self.assertTrue(found, "Created Invoice not found in the list response")

    def test_read(self):
        retrieved = self.api_client.get_invoice(self.invoice.id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.id, self.invoice.id)

    def test_write(self):
        data = {
            "contract": self.contract.id,
            "party": self.customer.id,
            "currency": self.currency.id,
            "staff": self.admin_user.id,
            "last_modified_by": self.admin_user.id,
            "description": "New API Invoice",
            "discount": "0.00",
            "payable_until": "2026-06-01",
            "payment_bank_reference": "API-REF-001",
            "status": "C",
        }
        created = self.api_client.create_invoice(data)
        self.assertIsNotNone(created)
        self.assertIsNotNone(created.id)

        db_obj = Invoice.objects.get(id=created.id)
        self.assertEqual(db_obj.description, "New API Invoice")
        self.assertEqual(db_obj.status, "C")

    def test_modify(self):
        updated = self.api_client.update_invoice(
            self.invoice.id, {"description": "Updated Invoice Description"}
        )
        self.assertIsNotNone(updated)
        self.assertEqual(updated.id, self.invoice.id)

        self.invoice.refresh_from_db()
        self.assertEqual(self.invoice.description, "Updated Invoice Description")
