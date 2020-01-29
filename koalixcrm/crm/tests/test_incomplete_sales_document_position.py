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
from koalixcrm.crm.factories.factory_customer_group import StandardCustomerGroupFactory, AdvancedCustomerGroupFactory
from koalixcrm.crm.factories.factory_tax import StandardTaxFactory
from koalixcrm.crm.factories.factory_unit import StandardUnitFactory, SmallUnitFactory
from koalixcrm.global_support_functions import make_date_utc
from koalixcrm.crm.models import SalesDocumentPosition


class DocumentSalesDocumentPosition(TestCase):
    def setUp(self):
        datetime_now = make_date_utc(datetime.datetime(2024, 1, 1, 0, 00))
        start_date = (datetime_now - datetime.timedelta(days=30)).date()
        end_date = (datetime_now + datetime.timedelta(days=30)).date()
        self.tax = StandardTaxFactory.create(tax_rate=10)
        self.test_currency_with_rounding = StandardCurrencyFactory.create(rounding=1)
        self.test_currency_without_rounding = StandardCurrencyFactory.create(
            rounding=None,
            description='Euro',
            short_name='EUR'
        )
        self.alternative_currency = self.test_currency_without_rounding
        self.customer_group = StandardCustomerGroupFactory.create()
        self.alternative_customer_group = AdvancedCustomerGroupFactory.create()
        self.customer = StandardCustomerFactory.create()
        self.customer.is_member_of.add(self.customer_group)
        self.customer.save()
        self.unit = StandardUnitFactory.create()
        self.alternative_unit = SmallUnitFactory.create()
        self.product_without_dates = StandardProductTypeFactory.create(
            product_type_identifier="A",
            tax=self.tax
        )
        self.price_without_customer_group = StandardPriceFactory.create(
            product_type=self.product_without_dates,
            customer_group=None,
            price=100,
            unit=self.unit,
            currency=self.test_currency_with_rounding,
            valid_from=start_date,
            valid_until=end_date
        )

    @pytest.mark.back_end_tests
    def test_calculate_document_price_overwritten(self):
        quote_1 = StandardQuoteFactory.create(customer=self.customer)
        StandardSalesDocumentPositionFactory.create(
            quantity=1,
            discount=0,
            product_type=self.product_without_dates,
            overwrite_product_price=True,
            position_price_per_unit=90,
            unit=self.unit,
            sales_document=quote_1
        )
        datetime_now = make_date_utc(datetime.datetime(2024, 1, 1, 0, 00))
        date_now = datetime_now.date()
        Calculations.calculate_document_price(
            document=quote_1,
            pricing_date=date_now)
        self.assertEqual(
            quote_1.last_calculated_price.__str__(), "90.00")
        self.assertEqual(
            quote_1.last_calculated_tax.__str__(), "9.00")

    @pytest.mark.back_end_tests
    def test_calculate_document_price_overwritten_WithNone(self):
        quote_2 = StandardQuoteFactory.create(customer=self.customer)
        StandardSalesDocumentPositionFactory.create(
            quantity=1,
            discount=0,
            product_type=self.product_without_dates,
            overwrite_product_price=True,
            position_price_per_unit=None,
            unit=self.unit,
            sales_document=quote_2
        )
        datetime_now = make_date_utc(datetime.datetime(2024, 1, 1, 0, 00))
        date_now = datetime_now.date()
        try:
            Calculations.calculate_document_price(
                document=quote_2,
                pricing_date=date_now)
        except SalesDocumentPosition.NoPriceFound as e:
            self.assertEqual(
                e.__str__(), "There is no Price set for the sales document position"
            )
