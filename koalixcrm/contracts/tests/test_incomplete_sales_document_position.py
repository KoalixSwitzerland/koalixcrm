import datetime

import pytest
from django.test import TestCase

from koalixcrm.contracts.models.calculations import Calculations
from koalixcrm.contracts.models.commercial_document_position import (
    CommercialDocumentPosition,
)
from koalixcrm.global_support_functions import make_date_utc
from koalixcrm.contacts.tests.factories.customer_factory import StandardCustomerFactory
from koalixcrm.contacts.tests.factories.customer_group_factory import (
    AdvancedCustomerGroupFactory,
    StandardCustomerGroupFactory,
)
from koalixcrm.contracts.tests.factories.commercial_document_position_factory import (
    StandardCommercialDocumentPositionFactory,
)
from koalixcrm.contracts.tests.factories.quotation_factory import StandardQuotationFactory
from koalixcrm.core.tests.factories.currency_factory import StandardCurrencyFactory
from koalixcrm.core.tests.factories.tax_factory import StandardTaxFactory
from koalixcrm.core.tests.factories.unit_factory import SmallUnitFactory, StandardUnitFactory
from koalixcrm.products.tests.factories.product_price_factory import StandardPriceFactory
from koalixcrm.products.tests.factories.product_type_factory import StandardProductTypeFactory


class DocumentCommercialDocumentPosition(TestCase):
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
        self.price_without_customer_group = StandardPriceFactory.create(
            product_type=self.product_without_dates,
            party_group=None,
            price=100,
            unit=self.unit,
            currency=self.test_currency_with_rounding,
            valid_from=start_date,
            valid_until=end_date
        )

    @pytest.mark.back_end_tests
    def test_calculate_document_price_overwritten(self):
        quotation_1 = StandardQuotationFactory.create(party=self.customer)
        StandardCommercialDocumentPositionFactory.create(
            quantity=1,
            discount=0,
            product_type=self.product_without_dates,
            overwrite_product_price=True,
            position_price_per_unit=90,
            unit=self.unit,
            commercial_document=quotation_1
        )
        datetime_now = make_date_utc(datetime.datetime(2024, 1, 1, 0, 00))
        date_now = datetime_now.date()
        Calculations.calculate_document_price(
            document=quotation_1,
            pricing_date=date_now)
        self.assertEqual(
            quotation_1.last_calculated_price.__str__(), "90.00")
        self.assertEqual(
            quotation_1.last_calculated_tax.__str__(), "9.00")

    @pytest.mark.back_end_tests
    def test_calculate_document_price_overwritten_WithNone(self):
        quotation_2 = StandardQuotationFactory.create(party=self.customer)
        StandardCommercialDocumentPositionFactory.create(
            quantity=1,
            discount=0,
            product_type=self.product_without_dates,
            overwrite_product_price=True,
            position_price_per_unit=None,
            unit=self.unit,
            commercial_document=quotation_2
        )
        datetime_now = make_date_utc(datetime.datetime(2024, 1, 1, 0, 00))
        date_now = datetime_now.date()
        try:
            Calculations.calculate_document_price(
                document=quotation_2,
                pricing_date=date_now)
        except CommercialDocumentPosition.NoPriceFound as e:
            self.assertEqual(
                e.__str__(), "There is no Price set for the commercial document position"
            )
