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
        cash = Account.objects.create(accountNumber="1000",
                                      title="Cash",
                                      accountType="A",
                                      description="Highest liquid asset",
                                      isopeninterestaccount=False,
                                      isopenreliabilitiesaccount=False,
                                      isProductInventoryActiva=False,
                                      isACustomerPaymentAccount=True)
        spendings = Account.objects.create(accountNumber="3000",
                                           title="Spendings",
                                           accountType="S",
                                           description="Purchase spendings",
                                           isopeninterestaccount=False,
                                           isopenreliabilitiesaccount=False,
                                           isProductInventoryActiva=False,
                                           isACustomerPaymentAccount=False)
        earnings = Account.objects.create(accountNumber="4000",
                                          title="Earnings",
                                          accountType="E",
                                          description="Sales account",
                                          isopeninterestaccount=False,
                                          isopenreliabilitiesaccount=False,
                                          isProductInventoryActiva=False,
                                          isACustomerPaymentAccount=False)
        datetime_now = datetime.datetime.today()
        from_date = (datetime_now - datetime.timedelta(days=30)).date()
        to_date = datetime_now.date()
        accounting_period = AccountingPeriod.objects.create(title="Fiscal year 2025",
                                                            begin=from_date,
                                                            end=to_date)
        Booking.objects.create(fromAccount=cash,
                               toAccount=spendings,
                               amount="1000",
                               description="This is the first booking",
                               bookingDate=datetime.date.today(),
                               accountingPeriod=accounting_period,
                               staff=user,
                               lastmodifiedby=user)

        Booking.objects.create(fromAccount=earnings,
                               toAccount=cash,
                               amount="500",
                               description="This is the first booking",
                               bookingDate=datetime.date.today(),
                               accountingPeriod=accounting_period,
                               staff=user,
                               lastmodifiedby=user)

    def test_sumOfAllBookings(self):
        cash_account = Account.objects.get(title="Cash")
        spendings_account = Account.objects.get(title="Spendings")
        earnings_account = Account.objects.get(title="Earnings")
        self.assertEqual((cash_account.sumOfAllBookings()).__str__(), "-500.00")
        self.assertEqual((spendings_account.sumOfAllBookings()).__str__(), "1000.00")
        self.assertEqual((earnings_account.sumOfAllBookings()).__str__(), "500.00")
