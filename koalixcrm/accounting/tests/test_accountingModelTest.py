from django.test import TestCase
from koalixcrm.accounting.models import Account
from koalixcrm.accounting.models import AccountingPeriod
from koalixcrm.accounting.models import Booking
from django.contrib.auth.models import User
import datetime


class AccountingModelTest(TestCase):
    def setUp(self):
        user = User.objects.create(username='Username',
                                   password="Userone")
        cash = Account.objects.create(account_number="1000",
                                      title="Cash",
                                      account_type="A",
                                      description="Highest liquid asset",
                                      is_open_interest_account=False,
                                      is_open_reliabilities_account=False,
                                      is_product_inventory_activa=False,
                                      is_a_customer_payment_account=True)
        spendings = Account.objects.create(account_number="3000",
                                           title="Spendings",
                                           account_type="S",
                                           description="Purchase spendings",
                                           is_open_interest_account=False,
                                           is_open_reliabilities_account=False,
                                           is_product_inventory_activa=False,
                                           is_a_customer_payment_account=False)
        earnings = Account.objects.create(account_number="4000",
                                          title="Earnings",
                                          account_type="E",
                                          description="Sales account",
                                          is_open_interest_account=False,
                                          is_open_reliabilities_account=False,
                                          is_product_inventory_activa=False,
                                          is_a_customer_payment_account=False)
        datetime_now = datetime.datetime(2024, 1, 1, 0, 00)
        from_date = datetime_now.date()
        to_date = (datetime_now + datetime.timedelta(days=365)).date()
        accounting_period_2024 = AccountingPeriod.objects.create(title="Fiscal year 2024",
                                                                 begin=from_date,
                                                                 end=to_date)
        from_date = to_date
        to_date = (datetime_now + datetime.timedelta(days=(365*2))).date()
        AccountingPeriod.objects.create(title="Fiscal year 2025",
                                        begin=from_date,
                                        end=to_date)
        from_date = to_date
        to_date = (datetime_now + datetime.timedelta(days=(365*3))).date()
        AccountingPeriod.objects.create(title="Fiscal year 2026",
                                        begin=from_date,
                                        end=to_date)
        Booking.objects.create(from_account=cash,
                               to_account=spendings,
                               amount="1000",
                               description="This is the first booking",
                               booking_date=datetime.date.today(),
                               accounting_period=accounting_period_2024,
                               staff=user,
                               last_modified_by=user)

        Booking.objects.create(from_account=earnings,
                               to_account=cash,
                               amount="500",
                               description="This is the first booking",
                               booking_date=datetime.date.today(),
                               accounting_period=accounting_period_2024,
                               staff=user,
                               last_modified_by=user)

    def test_sumOfAllBookings(self):
        cash_account = Account.objects.get(title="Cash")
        spendings_account = Account.objects.get(title="Spendings")
        earnings_account = Account.objects.get(title="Earnings")
        self.assertEqual((cash_account.sum_of_all_bookings()).__str__(), "-500.00")
        self.assertEqual((spendings_account.sum_of_all_bookings()).__str__(), "1000.00")
        self.assertEqual((earnings_account.sum_of_all_bookings()).__str__(), "500.00")

    def test_sumOfAllBookingsBeforeAccountPeriod(self):
        cash_account = Account.objects.get(title="Cash")
        spendings_account = Account.objects.get(title="Spendings")
        earnings_account = Account.objects.get(title="Earnings")
        accounting_period_2026 = AccountingPeriod.objects.get(title="Fiscal year 2026")
        self.assertEqual((cash_account.sum_of_all_bookings_before_accounting_period(accounting_period_2026)).__str__(), "-500.00")
        self.assertEqual((spendings_account.sum_of_all_bookings_before_accounting_period(accounting_period_2026)).__str__(), "1000.00")
        self.assertEqual((earnings_account.sum_of_all_bookings_before_accounting_period(accounting_period_2026)).__str__(), "500.00")

    def test_sumOfAllBookingsWithinAccountgPeriod(self):
        cash_account = Account.objects.get(title="Cash")
        spendings_account = Account.objects.get(title="Spendings")
        earnings_account = Account.objects.get(title="Earnings")
        accounting_period_2025 = AccountingPeriod.objects.get(title="Fiscal year 2025")
        self.assertEqual((cash_account.sum_of_all_bookings_within_accounting_period(accounting_period_2025)).__str__(), "0")
        self.assertEqual((spendings_account.sum_of_all_bookings_within_accounting_period(accounting_period_2025)).__str__(), "0")
        self.assertEqual((earnings_account.sum_of_all_bookings_within_accounting_period(accounting_period_2025)).__str__(), "0")