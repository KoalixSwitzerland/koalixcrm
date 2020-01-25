import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from koalixcrm.accounting.models import Account
from koalixcrm.accounting.models import AccountingPeriod
from koalixcrm.accounting.models import Booking
from koalixcrm.crm.documents.pdf_export import PDFExport
from koalixcrm.global_support_functions import make_date_utc


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
        bank_account = Account.objects.create(account_number="1300",
                                              title="Bank Account",
                                              account_type="A",
                                              description="Moderate liquid asset",
                                              is_open_interest_account=False,
                                              is_open_reliabilities_account=False,
                                              is_product_inventory_activa=False,
                                              is_a_customer_payment_account=True)
        bank_loan = Account.objects.create(account_number="2000",
                                      title="Shortterm bankloans",
                                      account_type="L",
                                      description="Shortterm loan",
                                      is_open_interest_account=False,
                                      is_open_reliabilities_account=False,
                                      is_product_inventory_activa=False,
                                      is_a_customer_payment_account=False)
        investment_capital = Account.objects.create(account_number="2900",
                                      title="Investment capital",
                                      account_type="L",
                                      description="Very longterm  loan",
                                      is_open_interest_account=False,
                                      is_open_reliabilities_account=False,
                                      is_product_inventory_activa=False,
                                      is_a_customer_payment_account=False)
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
        datetime_now = make_date_utc(datetime.datetime(2024, 1, 1, 0, 00))
        from_date = datetime_now.date()
        to_date = (datetime_now + datetime.timedelta(days=365)).date()
        accounting_period_2024 = AccountingPeriod.objects.create(title="Fiscal year 2024",
                                                                 begin=from_date,
                                                                 end=to_date)
        from_date = (datetime_now + datetime.timedelta(days=(365+1))).date()
        to_date = (datetime_now + datetime.timedelta(days=(365*2))).date()
        accounting_period_2025 = AccountingPeriod.objects.create(title="Fiscal year 2025",
                                        begin=from_date,
                                        end=to_date)
        from_date = (datetime_now + datetime.timedelta(days=(365*2+1))).date()
        to_date = (datetime_now + datetime.timedelta(days=(365*3))).date()
        AccountingPeriod.objects.create(title="Fiscal year 2026",
                                        begin=from_date,
                                        end=to_date)
        Booking.objects.create(from_account=cash,
                               to_account=spendings,
                               amount="1000",
                               description="This is the first booking",
                               booking_date=make_date_utc(datetime.datetime(2025, 1, 1, 0, 00)),
                               accounting_period=accounting_period_2025,
                               staff=user,
                               last_modified_by=user)

        Booking.objects.create(from_account=earnings,
                               to_account=cash,
                               amount="500",
                               description="This is the first booking",
                               booking_date=make_date_utc(datetime.datetime(2025, 1, 1, 0, 00)),
                               accounting_period=accounting_period_2025,
                               staff=user,
                               last_modified_by=user)

        Booking.objects.create(from_account=bank_loan,
                               to_account=cash,
                               amount="5000",
                               description="This is the first booking",
                               booking_date=make_date_utc(datetime.datetime(2025, 1, 1, 0, 00)),
                               accounting_period=accounting_period_2025,
                               staff=user,
                               last_modified_by=user)

        Booking.objects.create(from_account=investment_capital,
                               to_account=bank_account,
                               amount="490000",
                               description="This is the first booking",
                               booking_date=make_date_utc(datetime.datetime(2025, 1, 1, 0, 00)),
                               accounting_period=accounting_period_2024,
                               staff=user,
                               last_modified_by=user)

    def test_sumOfAllBookings(self):
        cash_account = Account.objects.get(title="Cash")
        spendings_account = Account.objects.get(title="Spendings")
        earnings_account = Account.objects.get(title="Earnings")
        self.assertEqual((cash_account.sum_of_all_bookings()).__str__(), "4500.00")
        self.assertEqual((spendings_account.sum_of_all_bookings()).__str__(), "1000.00")
        self.assertEqual((earnings_account.sum_of_all_bookings()).__str__(), "500.00")

    def test_sumOfAllBookingsBeforeAccountPeriod(self):
        cash_account = Account.objects.get(title="Cash")
        spendings_account = Account.objects.get(title="Spendings")
        earnings_account = Account.objects.get(title="Earnings")
        accounting_period_2026 = AccountingPeriod.objects.get(title="Fiscal year 2026")
        self.assertEqual((cash_account.sum_of_all_bookings_before_accounting_period(accounting_period_2026)).__str__(), "4500.00")
        self.assertEqual((spendings_account.sum_of_all_bookings_before_accounting_period(accounting_period_2026)).__str__(), "1000.00")
        self.assertEqual((earnings_account.sum_of_all_bookings_before_accounting_period(accounting_period_2026)).__str__(), "500.00")

    def test_sumOfAllBookingsWithinAccountgPeriod(self):
        cash_account = Account.objects.get(title="Cash")
        spendings_account = Account.objects.get(title="Spendings")
        earnings_account = Account.objects.get(title="Earnings")
        accounting_period_2024 = AccountingPeriod.objects.get(title="Fiscal year 2024")
        self.assertEqual((cash_account.sum_of_all_bookings_within_accounting_period(accounting_period_2024)).__str__(), "0")
        self.assertEqual((spendings_account.sum_of_all_bookings_within_accounting_period(accounting_period_2024)).__str__(), "0")
        self.assertEqual((earnings_account.sum_of_all_bookings_within_accounting_period(accounting_period_2024)).__str__(), "0")

    def test_overall_liabilities(self):
        accounting_period_2025 = AccountingPeriod.objects.get(title="Fiscal year 2025")
        self.assertEqual(
            (accounting_period_2025.overall_liabilities()).__str__(), "495000.00")

    def test_overall_assets(self):
        accounting_period_2025 = AccountingPeriod.objects.get(title="Fiscal year 2025")
        self.assertEqual(
            (accounting_period_2025.overall_assets()).__str__(), "494500.00")

    def test_overall_earnings(self):
        accounting_period_2025 = AccountingPeriod.objects.get(title="Fiscal year 2025")
        self.assertEqual(
            (accounting_period_2025.overall_earnings()).__str__(), "500.00")

    def test_overall_spendings(self):
        accounting_period_2025 = AccountingPeriod.objects.get(title="Fiscal year 2025")
        self.assertEqual(
            (accounting_period_2025.overall_spendings()).__str__(), "1000.00")

    def test_serialize_to_xml(self):
        accounting_period_2025 = AccountingPeriod.objects.get(title="Fiscal year 2025")
        xml = accounting_period_2025.serialize_to_xml()
        result=PDFExport.find_element_in_xml(xml, "object/[@model='accounting.account']/field[@name='title']", 'Earnings')
        self.assertEqual(result, 1)
        result=PDFExport.find_element_in_xml(xml, "object/[@model='accounting.account']/field[@name='title']", 'Spendings')
        self.assertEqual(result, 1)
        result=PDFExport.find_element_in_xml(xml, "object/[@model='accounting.account']/field[@name='title']", 'Investment capital')
        self.assertEqual(result, 1)
        result=PDFExport.find_element_in_xml(xml, "object/[@model='accounting.account']/field[@name='title']", 'Shortterm bankloans')
        self.assertEqual(result, 1)
        result=PDFExport.find_element_in_xml(xml, "object/[@model='accounting.account']/field[@name='title']",'Cash')
        self.assertEqual(result, 1)
        result=PDFExport.find_element_in_xml(xml, "object/[@model='accounting.account']/field[@name='title']",'Bank Account')
        self.assertEqual(result, 1)
        result=PDFExport.find_element_in_xml(xml, "object/[@model='accounting.accountingperiod']/Overall_Spendings", '1000.00')
        self.assertEqual(result, 1)
        result=PDFExport.find_element_in_xml(xml, "object/[@model='accounting.accountingperiod']/Overall_Earnings", '500.00')
        self.assertEqual(result, 1)
        result=PDFExport.find_element_in_xml(xml, "object/[@model='accounting.accountingperiod']/Overall_Assets", '494500.00')
        self.assertEqual(result, 1)
        result=PDFExport.find_element_in_xml(xml, "object/[@model='accounting.accountingperiod']/Overall_Liabilities", '495000.00')
        self.assertEqual(result, 1)
