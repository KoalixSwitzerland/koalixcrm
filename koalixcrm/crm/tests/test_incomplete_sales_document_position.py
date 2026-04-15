import pytest
import datetime
from django.test import TestCase
from koalixcrm.contracts.models.calculations import Calculations
from koalixcrm.settings.factory.currency_factory import StandardCurrencyFactory
from koalixcrm.contracts.factory.quote_factory import StandardQuoteFactory
from koalixcrm.contracts.factory.commercial_document_position_factory import StandardCommercialDocumentPositionFactory
from koalixcrm.products.factory.product_type_factory import StandardProductTypeFactory
from koalixcrm.products.factory.product_price_factory import StandardPriceFactory
from koalixcrm.crm.factory.customer_factory import StandardCustomerFactory
from koalixcrm.crm.factory.customer_group_factory import StandardCustomerGroupFactory, AdvancedCustomerGroupFactory
from koalixcrm.settings.factory.tax_factory import StandardTaxFactory
from koalixcrm.settings.factory.unit_factory import StandardUnitFactory, SmallUnitFactory
from koalixcrm.global_support_functions import make_date_utc
from koalixcrm.contracts.models.commercial_document_position import CommercialDocumentPosition


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
        StandardCommercialDocumentPositionFactory.create(
            quantity=1,
            discount=0,
            product_type=self.product_without_dates,
            overwrite_product_price=True,
            position_price_per_unit=90,
            unit=self.unit,
            commercial_document=quote_1
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
        StandardCommercialDocumentPositionFactory.create(
            quantity=1,
            discount=0,
            product_type=self.product_without_dates,
            overwrite_product_price=True,
            position_price_per_unit=None,
            unit=self.unit,
            commercial_document=quote_2
        )
        datetime_now = make_date_utc(datetime.datetime(2024, 1, 1, 0, 00))
        date_now = datetime_now.date()
        try:
            Calculations.calculate_document_price(
                document=quote_2,
                pricing_date=date_now)
        except CommercialDocumentPosition.NoPriceFound as e:
            self.assertEqual(
                e.__str__(), "There is no Price set for the commercial document position"
            )
