from django.test import TestCase
from django.contrib.auth.models import User
from koalixcrm.crm.models import Contract
from koalixcrm.crm.models import Customer
from koalixcrm.crm.models import CustomerGroup
from koalixcrm.crm.models import CustomerBillingCycle
from koalixcrm.crm.models import Currency
from koalixcrm.crm.models import Product
from koalixcrm.crm.models import Tax
from koalixcrm.crm.models import Unit
from koalixcrm.crm.models import Quote
from koalixcrm.crm.models import Price
from koalixcrm.crm.models import Task
from koalixcrm.crm.models import SalesDocumentPosition
from koalixcrm.crm.views.create_task import CreateTaskView
import datetime
import pytest


class DocumentCalculationsTest(TestCase):
    def setUp(self):
        datetime_now = datetime.datetime(2024, 1, 1, 0, 00)
        valid_from = (datetime_now - datetime.timedelta(days=30)).date()
        valid_until = (datetime_now + datetime.timedelta(days=30)).date()
        date_now = datetime_now.date()
        test_billing_cycle = CustomerBillingCycle.objects.create(
            name="30 days to pay",
            time_to_payment_date=30,
            payment_reminder_time_to_payment=10
        )
        test_user = User.objects.create(
            username='Username',
            password="User_one")
        test_customer_group = CustomerGroup.objects.create(
            name="Triple A"
        )
        test_customer = Customer.objects.create(
            name="John Smith",
            last_modified_by=test_user,
            default_customer_billing_cycle=test_billing_cycle,
        )
        test_customer.is_member_of = [test_customer_group]
        test_customer.save()
        test_currency = Currency.objects.create(
            description="Swiss Francs",
            short_name="CHF",
            rounding=0.05,
        )
        test_contract = Contract.objects.create(
            staff=test_user,
            description="This is a test contract",
            default_customer=test_customer,
            default_currency=test_currency,
            last_modification=date_now,
            last_modified_by=test_user
        )
        test_unit = Unit.objects.create(
            description="Kilogram",
            short_name="kg",
        )
        test_tax = Tax.objects.create(
            tax_rate=7.7,
            name="MwSt 7.7%")
        test_quote = Quote.objects.create(
            valid_until=valid_until,
            status="C",
            contract=test_contract,
            external_reference="ThisIsAnExternalReference",
            discount="11.23",
            description="This is a test offer",
            customer=test_customer,
            staff=test_user,
            currency=test_currency,
            date_of_creation=date_now,
            last_modified_by=test_user,)
        for i in range(10):
            test_product = Product.objects.create(
                description="This is a test product " + i.__str__(),
                title="This is a test product " + i.__str__(),
                product_number=12334235+i,
                default_unit=test_unit,
                last_modification=date_now,
                last_modified_by=test_user,
                tax=test_tax,
            )
            Price.objects.create(
                product=test_product,
                unit=test_unit,
                currency=test_currency,
                customer_group=test_customer_group,
                price=i*100,
                valid_from=valid_from,
                valid_until=valid_until,
            )
            SalesDocumentPosition.objects.create(
                sales_document=test_quote,
                position_number=i*10,
                quantity=0.333*i,
                description="This is a test position " + i.__str__(),
                discount=i*5,
                product=test_product,
                unit=test_unit,
                overwrite_product_price=False,
            )

    @pytest.mark.back_end_tests
    def test_create_task(self):
        test_quote = Quote.objects.get(description="This is a test offer")
        test_user = User.objects.get(username='Username')
        project = CreateTaskView.create_project_from_document(test_user, test_quote)
        tasks =Task.objects.filter(project=project.id)
        task_counter = 0
        for task_current in tasks:
            self.assertEqual(
                task_current.title.__str__()[:24], "This is a test position ")
            task_counter += 1
        self.assertEqual(
            task_counter.__str__(), "10")

