# -*- coding: utf-8 -*-

from django.test import LiveServerTestCase
from django.contrib.auth.models import User

from koalixcrm.accounting_api_py.accounting_api_client import KoalixCRMAccountingAPIClient
from koalixcrm.accounting.factory.booking_factory import StandardBookingFactory
from koalixcrm.accounting.factory.account_factory import StandardAccountFactory, OpenInterestAccountFactory
from koalixcrm.accounting.factory.accounting_period_factory import StandardAccountingPeriodFactory
from koalixcrm.accounting.models import Booking


class BookingAPITest(LiveServerTestCase):
    """Test for the Booking model API functionality."""

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword',
        )
        self.from_account = StandardAccountFactory.create()
        self.to_account = OpenInterestAccountFactory.create()
        self.accounting_period = StandardAccountingPeriodFactory.create()
        self.booking = StandardBookingFactory.create(
            from_account=self.from_account,
            to_account=self.to_account,
            accounting_period=self.accounting_period,
            staff=self.admin_user,
            last_modified_by=self.admin_user,
        )
        self.api_client = KoalixCRMAccountingAPIClient(
            self.live_server_url,
            username='admin',
            password='adminpassword',
        )

    def test_list(self):
        items = self.api_client.get_booking_list()
        self.assertGreaterEqual(len(items), 1)
        found = any(item.id == self.booking.id for item in items)
        self.assertTrue(found, "Created Booking not found in the list response")

    def test_read(self):
        retrieved = self.api_client.get_booking(self.booking.id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.id, self.booking.id)

    def test_write(self):
        data = {
            "fromAccount": {"id": self.from_account.id},
            "toAccount": {"id": self.to_account.id},
            "amount": "250.00",
            "description": "API test booking",
            "bookingDate": "2018-07-01T00:00",
            "bookingReference": None,
            "accountingPeriod": {"id": self.accounting_period.id},
        }
        created = self.api_client.create_booking(data)
        self.assertIsNotNone(created)
        self.assertIsNotNone(created.id)

        db_obj = Booking.objects.get(id=created.id)
        self.assertEqual(db_obj.description, "API test booking")

    def test_modify(self):
        updated = self.api_client.update_booking(
            self.booking.id, {"description": "Updated booking description"}
        )
        self.assertIsNotNone(updated)
        self.assertEqual(updated.id, self.booking.id)

        self.booking.refresh_from_db()
        self.assertEqual(self.booking.description, "Updated booking description")
