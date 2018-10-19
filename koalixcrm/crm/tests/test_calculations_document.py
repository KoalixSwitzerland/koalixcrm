import pytest
import datetime
from django.test import TestCase
from koalixcrm.crm.documents.calculations import Calculations
from koalixcrm.crm.factories.factory_currency import StandardCurrencyFactory
from koalixcrm.crm.factories.factory_quote import StandardQuoteFactory
from koalixcrm.crm.factories.factory_sales_document_position import StandardSalesDocumentPositionFactory
from koalixcrm.crm.factories.factory_product_type import StandardProductTypeFactory
from koalixcrm.crm.factories.factory_product_price import StandardPriceFactory
from koalixcrm.crm.factories.factory_customer import StandardCustomerFactory
from koalixcrm.crm.factories.factory_tax import StandardTaxFactory
from koalixcrm.test_support_functions import make_date_utc


class DocumentCalculationsTest(TestCase):
    def setUp(self):
        datetime_now = make_date_utc(datetime.datetime(2024, 1, 1, 0, 00))
        start_date = (datetime_now - datetime.timedelta(days=30)).date()
        end_date = (datetime_now + datetime.timedelta(days=30)).date()
        self.tax = StandardTaxFactory.create(tax_rate=10)
        self.test_currency_with_rounding = StandardCurrencyFactory.create()
        self.test_currency_without_rounding = StandardCurrencyFactory.create(rounding=None)
        self.customer = StandardCustomerFactory.create()
        self.product_without_dates = StandardProductTypeFactory.create(
            product_type_identifier="A",
            tax=self.tax
        )
        self.product_without_date_from = StandardProductTypeFactory.create(
            product_type_identifier="B",
            tax=self.tax
        )
        self.product_without_date_to = StandardProductTypeFactory.create(
            product_type_identifier="C",
            tax=self.tax
        )
        self.product_without_customer_group = StandardProductTypeFactory.create(
            product_type_identifier="D",
            tax=self.tax
        )
        self.product_with_currency_rounding = StandardProductTypeFactory.create(
            product_type_identifier="E",
            tax=self.tax
        )
        self.product_without_currency_rounding = StandardProductTypeFactory.create(
            product_type_identifier="F",
            tax=self.tax
        )
        self.price_without_customer_group = StandardPriceFactory.create(
            product_type=self.product_without_customer_group,
            customer_group=None,
            price=100,
            valid_from=start_date,
            valid_until=end_date
        )
        self.price_without_dates = StandardPriceFactory.create(
            product_type=self.product_without_dates,
            valid_from=None,
            valid_until=None,
            price=80
        )
        self.price_without_date_to = StandardPriceFactory.create(
            product_type=self.product_without_date_to,
            valid_from=start_date,
            valid_until=None,
            price=130
        )
        self.price_without_date_from = StandardPriceFactory.create(
            product_type=self.product_without_date_from,
            valid_from=None,
            valid_until=end_date,
            price=50
        )
        self.price_without_date_from = StandardPriceFactory.create(
            product_type=self.product_without_currency_rounding,
            currency=self.test_currency_without_rounding,
            price=25,
            valid_from=start_date,
            valid_until=end_date
        )
        self.price_without_date_from = StandardPriceFactory.create(
            product_type=self.product_with_currency_rounding,
            currency=self.test_currency_with_rounding,
            price=33,
            valid_from=start_date,
            valid_until=end_date
        )

    @pytest.mark.back_end_tests
    def test_calculate_document_price(self):
        quote_1 = StandardQuoteFactory.create()
        StandardSalesDocumentPositionFactory.create(
            quantity=1,
            discount=0,
            product_type=self.product_without_customer_group,
            overwrite_product_price=False,
            sales_document=quote_1
        )
        datetime_now = datetime.datetime(2024, 1, 1, 0, 00)
        date_now = datetime_now.date()
        Calculations.calculate_document_price(
            document=quote_1,
            pricing_date=date_now)
        self.assertEqual(
            quote_1.last_calculated_price.__str__(), "90.00")
        self.assertEqual(
            quote_1.last_calculated_tax.__str__(), "10.00")

        quote_2 = StandardQuoteFactory.create()
        StandardSalesDocumentPositionFactory.create(
            quantity=1,
            discount=0,
            product_type=self.product_without_date_from,
            overwrite_product_price=False,
            sales_document=quote_2
        )
        datetime_now = datetime.datetime(2024, 1, 1, 0, 00)
        date_now = datetime_now.date()
        Calculations.calculate_document_price(
            document=quote_2,
            pricing_date=date_now)
        self.assertEqual(
            quote_2.last_calculated_price.__str__(), "72.00")
        self.assertEqual(
            quote_2.last_calculated_tax.__str__(), "8.00")
