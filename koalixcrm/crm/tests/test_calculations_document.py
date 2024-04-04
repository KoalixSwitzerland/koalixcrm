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
from koalixcrm.crm.factories.factory_customer_group_transform import StandardCustomerGroupTransformFactory
from koalixcrm.crm.factories.factory_unit_transform import StandardUnitTransformFactory
from koalixcrm.crm.factories.factory_currency_transform import StandardCurrencyTransformFactory
from koalixcrm.global_support_functions import make_date_utc


class DocumentCalculationsTest(TestCase):
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
        self.product_without_date_from = StandardProductTypeFactory.create(
            product_type_identifier="B",
            tax=self.tax
        )
        self.product_without_date_until = StandardProductTypeFactory.create(
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
        self.product_with_alternative_customer_group = StandardProductTypeFactory.create(
            product_type_identifier="G",
            tax=self.tax
        )
        self.product_with_alternative_unit = StandardProductTypeFactory.create(
            product_type_identifier="H",
            tax=self.tax
        )
        self.product_with_alternative_currency = StandardProductTypeFactory.create(
            product_type_identifier="I",
            tax=self.tax
        )
        self.price_without_customer_group = StandardPriceFactory.create(
            product_type=self.product_without_customer_group,
            customer_group=None,
            price=100,
            unit=self.unit,
            currency=self.test_currency_with_rounding,
            valid_from=start_date,
            valid_until=end_date
        )
        self.price_without_dates = StandardPriceFactory.create(
            product_type=self.product_without_dates,
            customer_group=self.customer_group,
            valid_from=None,
            valid_until=None,
            unit=self.unit,
            currency=self.test_currency_with_rounding,
            price=80
        )
        self.price_without_date_to = StandardPriceFactory.create(
            product_type=self.product_without_date_until,
            customer_group=self.customer_group,
            valid_from=start_date,
            valid_until=None,
            unit=self.unit,
            currency=self.test_currency_with_rounding,
            price=130
        )
        self.price_without_date_from = StandardPriceFactory.create(
            product_type=self.product_without_date_from,
            customer_group=self.customer_group,
            valid_from=None,
            valid_until=end_date,
            unit=self.unit,
            currency=self.test_currency_with_rounding,
            price=50
        )
        self.price_without_date_from = StandardPriceFactory.create(
            product_type=self.product_without_currency_rounding,
            currency=self.test_currency_without_rounding,
            customer_group=self.customer_group,
            price=25,
            unit=self.unit,
            valid_from=start_date,
            valid_until=end_date
        )
        self.price_without_date_from = StandardPriceFactory.create(
            product_type=self.product_with_currency_rounding,
            currency=self.test_currency_with_rounding,
            customer_group=self.customer_group,
            price=33,
            unit=self.unit,
            valid_from=start_date,
            valid_until=end_date
        )
        self.price_with_alternative_customer_group = StandardPriceFactory.create(
            product_type=self.product_with_alternative_customer_group,
            customer_group=self.alternative_customer_group,
            valid_from=start_date,
            valid_until=end_date,
            unit=self.unit,
            currency=self.test_currency_with_rounding,
            price=80
        )
        self.customer_group_transform = StandardCustomerGroupTransformFactory.create(
            from_customer_group=self.alternative_customer_group,
            to_customer_group=self.customer_group,
            product_type=self.product_with_alternative_customer_group,
            factor=0.50
        )
        self.price_with_alternative_currency = StandardPriceFactory.create(
            product_type=self.product_with_alternative_currency,
            customer_group=self.customer_group,
            valid_from=start_date,
            valid_until=end_date,
            unit=self.unit,
            currency=self.alternative_currency,
            price=80
        )
        self.currency_transform = StandardCurrencyTransformFactory.create(
            from_currency=self.alternative_currency,
            to_currency=self.test_currency_with_rounding,
            product_type=self.product_with_alternative_currency,
            factor=0.50
        )
        self.price_with_alternative_unit = StandardPriceFactory.create(
            product_type=self.product_with_alternative_unit,
            customer_group=self.customer_group,
            valid_from=start_date,
            valid_until=end_date,
            unit=self.alternative_unit,
            currency=self.test_currency_with_rounding,
            price=80
        )
        self.currency_transform = StandardUnitTransformFactory.create(
            from_unit=self.alternative_unit,
            to_unit=self.unit,
            product_type=self.product_with_alternative_unit,
            factor=0.50
        )

    @pytest.mark.back_end_tests
    def test_calculate_document_price_without_customer_group(self):
        quote_1 = StandardQuoteFactory.create(customer=self.customer)
        StandardSalesDocumentPositionFactory.create(
            quantity=1,
            discount=0,
            product_type=self.product_without_customer_group,
            overwrite_product_price=False,
            unit=self.unit,
            sales_document=quote_1
        )
        datetime_now = make_date_utc(datetime.datetime(2024, 1, 1, 0, 00))
        date_now = datetime_now.date()
        Calculations.calculate_document_price(
            document=quote_1,
            pricing_date=date_now)
        self.assertEqual(
            quote_1.last_calculated_price.__str__(), "100.00")
        self.assertEqual(
            quote_1.last_calculated_tax.__str__(), "10.00")

    @pytest.mark.back_end_tests
    def test_calculate_document_price_without_date_from(self):
        quote_2 = StandardQuoteFactory.create(customer=self.customer)
        StandardSalesDocumentPositionFactory.create(
            quantity=1,
            discount=0,
            unit=self.unit,
            product_type=self.product_without_date_from,
            overwrite_product_price=False,
            sales_document=quote_2
        )
        datetime_now = make_date_utc(datetime.datetime(2024, 1, 1, 0, 00))
        date_now = datetime_now.date()
        Calculations.calculate_document_price(
            document=quote_2,
            pricing_date=date_now)
        self.assertEqual(
            quote_2.last_calculated_price.__str__(), "50.00")
        self.assertEqual(
            quote_2.last_calculated_tax.__str__(), "5.00")

    @pytest.mark.back_end_tests
    def test_calculate_document_price_without_date_until(self):
        quote_3 = StandardQuoteFactory.create(customer=self.customer)
        StandardSalesDocumentPositionFactory.create(
            quantity=1,
            discount=0,
            unit=self.unit,
            product_type=self.product_without_date_until,
            overwrite_product_price=False,
            sales_document=quote_3
        )
        datetime_now = make_date_utc(datetime.datetime(2024, 1, 1, 0, 00))
        date_now = datetime_now.date()
        Calculations.calculate_document_price(
            document=quote_3,
            pricing_date=date_now)
        self.assertEqual(
            quote_3.last_calculated_price.__str__(), "130.00")
        self.assertEqual(
            quote_3.last_calculated_tax.__str__(), "13.00")

    @pytest.mark.back_end_tests
    def test_calculate_document_price_without_dates(self):
        quote_4 = StandardQuoteFactory.create(customer=self.customer)
        StandardSalesDocumentPositionFactory.create(
            quantity=1,
            discount=0,
            unit=self.unit,
            product_type=self.product_without_dates,
            overwrite_product_price=False,
            sales_document=quote_4
        )
        datetime_now = make_date_utc(datetime.datetime(2024, 1, 1, 0, 00))
        date_now = datetime_now.date()
        Calculations.calculate_document_price(
            document=quote_4,
            pricing_date=date_now)
        self.assertEqual(
            quote_4.last_calculated_price.__str__(), "80.00")
        self.assertEqual(
            quote_4.last_calculated_tax.__str__(), "8.00")

    @pytest.mark.back_end_tests
    def test_calculate_document_price_with_currency_rounding(self):
        quote_5 = StandardQuoteFactory.create(
            customer=self.customer,
            currency=self.test_currency_with_rounding
        )
        StandardSalesDocumentPositionFactory.create(
            quantity=1,
            discount=7.5,
            unit=self.unit,
            product_type=self.product_with_currency_rounding,
            overwrite_product_price=False,
            sales_document=quote_5
        )
        datetime_now = make_date_utc(datetime.datetime(2024, 1, 1, 0, 00))
        date_now = datetime_now.date()
        Calculations.calculate_document_price(
            document=quote_5,
            pricing_date=date_now)
        self.assertEqual(
            quote_5.last_calculated_price.__str__(), "30")
        self.assertEqual(
            quote_5.last_calculated_tax.__str__(), "3")

    @pytest.mark.back_end_tests
    def test_calculate_document_price_without_currency_rounding(self):
        quote_6 = StandardQuoteFactory.create(
            customer=self.customer,
            currency=self.test_currency_without_rounding
        )
        StandardSalesDocumentPositionFactory.create(
            quantity=1,
            discount=7.5,
            unit=self.unit,
            product_type=self.product_without_currency_rounding,
            overwrite_product_price=False,
            sales_document=quote_6
        )
        datetime_now = make_date_utc(datetime.datetime(2024, 1, 1, 0, 00))
        date_now = datetime_now.date()
        Calculations.calculate_document_price(
            document=quote_6,
            pricing_date=date_now)
        self.assertEqual(
            quote_6.last_calculated_price.__str__(), "23.10")
        self.assertEqual(
            quote_6.last_calculated_tax.__str__(), "2.30")

    @pytest.mark.back_end_tests
    def test_calculate_document_price_with_document_discount(self):
        quote_7 = StandardQuoteFactory.create(
            customer=self.customer,
            currency=self.test_currency_without_rounding,
            discount=10
        )
        StandardSalesDocumentPositionFactory.create(
            quantity=1,
            discount=7.5,
            unit=self.unit,
            product_type=self.product_without_currency_rounding,
            overwrite_product_price=False,
            sales_document=quote_7
        )
        datetime_now = make_date_utc(datetime.datetime(2024, 1, 1, 0, 00))
        date_now = datetime_now.date()
        Calculations.calculate_document_price(
            document=quote_7,
            pricing_date=date_now)
        self.assertEqual(
            quote_7.last_calculated_price.__str__(), "20.80")
        self.assertEqual(
            quote_7.last_calculated_tax.__str__(), "2.05")

    @pytest.mark.back_end_tests
    def test_calculate_document_with_customer_group_transform(self):
        quote_8 = StandardQuoteFactory.create(
            customer=self.customer)
        StandardSalesDocumentPositionFactory.create(
            quantity=1,
            discount=0,
            unit=self.unit,
            product_type=self.product_with_alternative_customer_group,
            overwrite_product_price=False,
            sales_document=quote_8
        )
        datetime_now = make_date_utc(datetime.datetime(2024, 1, 1, 0, 00))
        date_now = datetime_now.date()
        Calculations.calculate_document_price(
            document=quote_8,
            pricing_date=date_now)
        self.assertEqual(
            quote_8.last_calculated_price.__str__(), "40.00")
        self.assertEqual(
            quote_8.last_calculated_tax.__str__(), "4.00")

    @pytest.mark.back_end_tests
    def test_calculate_document_with_currency_transform(self):
        quote_9 = StandardQuoteFactory.create(
            currency=self.test_currency_with_rounding,
            customer=self.customer)
        StandardSalesDocumentPositionFactory.create(
            quantity=1,
            discount=0,
            unit=self.unit,
            product_type=self.product_with_alternative_currency,
            overwrite_product_price=False,
            sales_document=quote_9
        )
        datetime_now = make_date_utc(datetime.datetime(2024, 1, 1, 0, 00))
        date_now = datetime_now.date()
        Calculations.calculate_document_price(
            document=quote_9,
            pricing_date=date_now)
        self.assertEqual(
            quote_9.last_calculated_price.__str__(), "40")
        self.assertEqual(
            quote_9.last_calculated_tax.__str__(), "4")

    @pytest.mark.back_end_tests
    def test_calculate_document_with_unit_transform(self):
        quote_10 = StandardQuoteFactory.create(customer=self.customer)
        StandardSalesDocumentPositionFactory.create(
            quantity=1,
            discount=0,
            unit=self.unit,
            product_type=self.product_with_alternative_unit,
            overwrite_product_price=False,
            sales_document=quote_10
        )
        datetime_now = make_date_utc(datetime.datetime(2024, 1, 1, 0, 00))
        date_now = datetime_now.date()
        Calculations.calculate_document_price(
            document=quote_10,
            pricing_date=date_now)
        self.assertEqual(
            quote_10.last_calculated_price.__str__(), "40.00")
        self.assertEqual(
            quote_10.last_calculated_tax.__str__(), "4.00")
