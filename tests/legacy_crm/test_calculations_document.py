import datetime

import pytest
from django.test import TestCase

from koalixcrm.contracts.models.calculations import Calculations
from koalixcrm.global_support_functions import make_date_utc
from tests.factories.contacts.customer_factory import StandardCustomerFactory
from tests.factories.contacts.customer_group_factory import (
    AdvancedCustomerGroupFactory,
    StandardCustomerGroupFactory,
)
from tests.factories.contracts.commercial_document_position_factory import (
    StandardCommercialDocumentPositionFactory,
)
from tests.factories.contracts.quotation_factory import StandardQuotationFactory
from tests.factories.core.currency_factory import StandardCurrencyFactory
from tests.factories.core.currency_transform_factory import (
    StandardCurrencyTransformFactory,
)
from tests.factories.core.tax_factory import StandardTaxFactory
from tests.factories.core.unit_factory import SmallUnitFactory, StandardUnitFactory
from tests.factories.core.unit_transform_factory import StandardUnitTransformFactory
from tests.factories.products.customer_group_transform_factory import (
    StandardCustomerGroupTransformFactory,
)
from tests.factories.products.product_price_factory import StandardPriceFactory
from tests.factories.products.product_type_factory import StandardProductTypeFactory


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
        self.customer = StandardCustomerFactory.create(
            is_member_of=(self.customer_group,),
        )
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
            party_group=None,
            price=100,
            unit=self.unit,
            currency=self.test_currency_with_rounding,
            valid_from=start_date,
            valid_until=end_date
        )
        self.price_without_dates = StandardPriceFactory.create(
            product_type=self.product_without_dates,
            party_group=self.customer_group,
            valid_from=None,
            valid_until=None,
            unit=self.unit,
            currency=self.test_currency_with_rounding,
            price=80
        )
        self.price_without_date_to = StandardPriceFactory.create(
            product_type=self.product_without_date_until,
            party_group=self.customer_group,
            valid_from=start_date,
            valid_until=None,
            unit=self.unit,
            currency=self.test_currency_with_rounding,
            price=130
        )
        self.price_without_date_from = StandardPriceFactory.create(
            product_type=self.product_without_date_from,
            party_group=self.customer_group,
            valid_from=None,
            valid_until=end_date,
            unit=self.unit,
            currency=self.test_currency_with_rounding,
            price=50
        )
        self.price_without_date_from = StandardPriceFactory.create(
            product_type=self.product_without_currency_rounding,
            currency=self.test_currency_without_rounding,
            party_group=self.customer_group,
            price=25,
            unit=self.unit,
            valid_from=start_date,
            valid_until=end_date
        )
        self.price_without_date_from = StandardPriceFactory.create(
            product_type=self.product_with_currency_rounding,
            currency=self.test_currency_with_rounding,
            party_group=self.customer_group,
            price=33,
            unit=self.unit,
            valid_from=start_date,
            valid_until=end_date
        )
        self.price_with_alternative_customer_group = StandardPriceFactory.create(
            product_type=self.product_with_alternative_customer_group,
            party_group=self.alternative_customer_group,
            valid_from=start_date,
            valid_until=end_date,
            unit=self.unit,
            currency=self.test_currency_with_rounding,
            price=80
        )
        self.customer_group_transform = StandardCustomerGroupTransformFactory.create(
            from_party_group=self.alternative_customer_group,
            to_party_group=self.customer_group,
            product_type=self.product_with_alternative_customer_group,
            factor=0.50
        )
        self.price_with_alternative_currency = StandardPriceFactory.create(
            product_type=self.product_with_alternative_currency,
            party_group=self.customer_group,
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
            party_group=self.customer_group,
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
        quotation_1 = StandardQuotationFactory.create(party=self.customer)
        StandardCommercialDocumentPositionFactory.create(
            quantity=1,
            discount=0,
            product_type=self.product_without_customer_group,
            overwrite_product_price=False,
            unit=self.unit,
            commercial_document=quotation_1
        )
        datetime_now = make_date_utc(datetime.datetime(2024, 1, 1, 0, 00))
        date_now = datetime_now.date()
        Calculations.calculate_document_price(
            document=quotation_1,
            pricing_date=date_now)
        self.assertEqual(
            quotation_1.last_calculated_price.__str__(), "100.00")
        self.assertEqual(
            quotation_1.last_calculated_tax.__str__(), "10.00")

    @pytest.mark.back_end_tests
    def test_calculate_document_price_without_date_from(self):
        quotation_2 = StandardQuotationFactory.create(party=self.customer)
        StandardCommercialDocumentPositionFactory.create(
            quantity=1,
            discount=0,
            unit=self.unit,
            product_type=self.product_without_date_from,
            overwrite_product_price=False,
            commercial_document=quotation_2
        )
        datetime_now = make_date_utc(datetime.datetime(2024, 1, 1, 0, 00))
        date_now = datetime_now.date()
        Calculations.calculate_document_price(
            document=quotation_2,
            pricing_date=date_now)
        self.assertEqual(
            quotation_2.last_calculated_price.__str__(), "50.00")
        self.assertEqual(
            quotation_2.last_calculated_tax.__str__(), "5.00")

    @pytest.mark.back_end_tests
    def test_calculate_document_price_without_date_until(self):
        quotation_3 = StandardQuotationFactory.create(party=self.customer)
        StandardCommercialDocumentPositionFactory.create(
            quantity=1,
            discount=0,
            unit=self.unit,
            product_type=self.product_without_date_until,
            overwrite_product_price=False,
            commercial_document=quotation_3
        )
        datetime_now = make_date_utc(datetime.datetime(2024, 1, 1, 0, 00))
        date_now = datetime_now.date()
        Calculations.calculate_document_price(
            document=quotation_3,
            pricing_date=date_now)
        self.assertEqual(
            quotation_3.last_calculated_price.__str__(), "130.00")
        self.assertEqual(
            quotation_3.last_calculated_tax.__str__(), "13.00")

    @pytest.mark.back_end_tests
    def test_calculate_document_price_without_dates(self):
        quotation_4 = StandardQuotationFactory.create(party=self.customer)
        StandardCommercialDocumentPositionFactory.create(
            quantity=1,
            discount=0,
            unit=self.unit,
            product_type=self.product_without_dates,
            overwrite_product_price=False,
            commercial_document=quotation_4
        )
        datetime_now = make_date_utc(datetime.datetime(2024, 1, 1, 0, 00))
        date_now = datetime_now.date()
        Calculations.calculate_document_price(
            document=quotation_4,
            pricing_date=date_now)
        self.assertEqual(
            quotation_4.last_calculated_price.__str__(), "80.00")
        self.assertEqual(
            quotation_4.last_calculated_tax.__str__(), "8.00")

    @pytest.mark.back_end_tests
    def test_calculate_document_price_with_currency_rounding(self):
        quotation_5 = StandardQuotationFactory.create(
            party=self.customer,
            currency=self.test_currency_with_rounding
        )
        StandardCommercialDocumentPositionFactory.create(
            quantity=1,
            discount=7.5,
            unit=self.unit,
            product_type=self.product_with_currency_rounding,
            overwrite_product_price=False,
            commercial_document=quotation_5
        )
        datetime_now = make_date_utc(datetime.datetime(2024, 1, 1, 0, 00))
        date_now = datetime_now.date()
        Calculations.calculate_document_price(
            document=quotation_5,
            pricing_date=date_now)
        self.assertEqual(
            quotation_5.last_calculated_price.__str__(), "30")
        self.assertEqual(
            quotation_5.last_calculated_tax.__str__(), "3")

    @pytest.mark.back_end_tests
    def test_calculate_document_price_without_currency_rounding(self):
        quotation_6 = StandardQuotationFactory.create(
            party=self.customer,
            currency=self.test_currency_without_rounding
        )
        StandardCommercialDocumentPositionFactory.create(
            quantity=1,
            discount=7.5,
            unit=self.unit,
            product_type=self.product_without_currency_rounding,
            overwrite_product_price=False,
            commercial_document=quotation_6
        )
        datetime_now = make_date_utc(datetime.datetime(2024, 1, 1, 0, 00))
        date_now = datetime_now.date()
        Calculations.calculate_document_price(
            document=quotation_6,
            pricing_date=date_now)
        self.assertEqual(
            quotation_6.last_calculated_price.__str__(), "23.10")
        self.assertEqual(
            quotation_6.last_calculated_tax.__str__(), "2.30")

    @pytest.mark.back_end_tests
    def test_calculate_document_price_with_document_discount(self):
        quotation_7 = StandardQuotationFactory.create(
            party=self.customer,
            currency=self.test_currency_without_rounding,
            discount=10
        )
        StandardCommercialDocumentPositionFactory.create(
            quantity=1,
            discount=7.5,
            unit=self.unit,
            product_type=self.product_without_currency_rounding,
            overwrite_product_price=False,
            commercial_document=quotation_7
        )
        datetime_now = make_date_utc(datetime.datetime(2024, 1, 1, 0, 00))
        date_now = datetime_now.date()
        Calculations.calculate_document_price(
            document=quotation_7,
            pricing_date=date_now)
        self.assertEqual(
            quotation_7.last_calculated_price.__str__(), "20.80")
        self.assertEqual(
            quotation_7.last_calculated_tax.__str__(), "2.05")

    @pytest.mark.back_end_tests
    def test_calculate_document_with_customer_group_transform(self):
        quotation_8 = StandardQuotationFactory.create(
            party=self.customer)
        StandardCommercialDocumentPositionFactory.create(
            quantity=1,
            discount=0,
            unit=self.unit,
            product_type=self.product_with_alternative_customer_group,
            overwrite_product_price=False,
            commercial_document=quotation_8
        )
        datetime_now = make_date_utc(datetime.datetime(2024, 1, 1, 0, 00))
        date_now = datetime_now.date()
        Calculations.calculate_document_price(
            document=quotation_8,
            pricing_date=date_now)
        self.assertEqual(
            quotation_8.last_calculated_price.__str__(), "40.00")
        self.assertEqual(
            quotation_8.last_calculated_tax.__str__(), "4.00")

    @pytest.mark.back_end_tests
    def test_calculate_document_with_currency_transform(self):
        quotation_9 = StandardQuotationFactory.create(
            currency=self.test_currency_with_rounding,
            party=self.customer)
        StandardCommercialDocumentPositionFactory.create(
            quantity=1,
            discount=0,
            unit=self.unit,
            product_type=self.product_with_alternative_currency,
            overwrite_product_price=False,
            commercial_document=quotation_9
        )
        datetime_now = make_date_utc(datetime.datetime(2024, 1, 1, 0, 00))
        date_now = datetime_now.date()
        Calculations.calculate_document_price(
            document=quotation_9,
            pricing_date=date_now)
        self.assertEqual(
            quotation_9.last_calculated_price.__str__(), "40")
        self.assertEqual(
            quotation_9.last_calculated_tax.__str__(), "4")

    @pytest.mark.back_end_tests
    def test_calculate_document_with_unit_transform(self):
        quotation_10 = StandardQuotationFactory.create(party=self.customer)
        StandardCommercialDocumentPositionFactory.create(
            quantity=1,
            discount=0,
            unit=self.unit,
            product_type=self.product_with_alternative_unit,
            overwrite_product_price=False,
            commercial_document=quotation_10
        )
        datetime_now = make_date_utc(datetime.datetime(2024, 1, 1, 0, 00))
        date_now = datetime_now.date()
        Calculations.calculate_document_price(
            document=quotation_10,
            pricing_date=date_now)
        self.assertEqual(
            quotation_10.last_calculated_price.__str__(), "40.00")
        self.assertEqual(
            quotation_10.last_calculated_tax.__str__(), "4.00")
