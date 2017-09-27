from unittest import TestCase

from apps.accounting.models import Account


class AccountingModelTest(TestCase):

    def test_sumOfAllBookings(self):
        account = Account(
            accountNumber=1234,
            title="Account1234")

        assert account.accountNumber == 1234
        assert account.title == "Account1234"
