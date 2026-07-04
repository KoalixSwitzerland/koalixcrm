# -*- coding: utf-8 -*-
"""ADR-0005 (+ Amendment 2026-06-28 / ADR-0021), REQ-0011, REQ-0012:
`PriceList`, `ProductPrice` re-keyed to `ProductVariant`, three-level price
precedence, `customer_group_transform` still applies on top."""
import datetime

import pytest
from django.db import IntegrityError, transaction
from django.test import TestCase

from koalixcrm.products.models.price_list import PriceList
from koalixcrm.products.models.product_price import ProductPrice
from koalixcrm.products.services.price_resolution import NoPriceFound, resolve_price
from tests.factories.contacts.customer_group_factory import StandardCustomerGroupFactory
from tests.factories.core.currency_factory import StandardCurrencyFactory
from tests.factories.core.unit_factory import StandardUnitFactory
from tests.factories.core.workspace_factory import DefaultWorkspaceFactory
from tests.factories.products.customer_group_transform_factory import (
    StandardCustomerGroupTransformFactory,
)
from tests.factories.products.price_list_factory import StandardPriceListFactory
from tests.factories.products.product_price_factory import StandardPriceFactory
from tests.factories.products.product_type_factory import StandardProductTypeFactory
from tests.factories.products.product_variant_factory import (
    StandardProductVariantFactory,
)


class ProductPriceKeyedToVariantTest(TestCase):
    @pytest.mark.back_end_tests
    def test_product_price_fk_points_at_variant(self):
        field = ProductPrice._meta.get_field("variant")
        self.assertEqual(field.related_model.__name__, "ProductVariant")
        self.assertFalse(hasattr(ProductPrice, "product_type"))

    @pytest.mark.back_end_tests
    def test_two_variants_of_same_product_carry_independent_prices(self):
        product = StandardProductTypeFactory.create()
        small = StandardProductVariantFactory.create(product=product, sku="SKU-250G")
        large = StandardProductVariantFactory.create(product=product, sku="SKU-500G")
        StandardPriceFactory.create(variant=small, price="2.50")
        StandardPriceFactory.create(variant=large, price="4.50")
        self.assertEqual(small.prices.get().price.__str__(), "2.50")
        self.assertEqual(large.prices.get().price.__str__(), "4.50")

    @pytest.mark.back_end_tests
    def test_product_get_price_aggregates_across_variants(self):
        """`Product.get_price` is a compatibility shim over
        `variant__product` — used by `contracts.Calculations`, which is not
        yet variant-aware."""
        product = StandardProductTypeFactory.create()
        variant = StandardProductVariantFactory.create(product=product, sku="SKU-AGG")
        unit = StandardUnitFactory.create()
        currency = StandardCurrencyFactory.create()
        StandardPriceFactory.create(
            variant=variant, price="9.99", unit=unit, currency=currency,
            party_group=None, valid_from=None, valid_until=None,
        )
        price = product.get_price(datetime.date(2024, 1, 1), unit, None, currency)
        self.assertEqual(str(price), "9.99")


class PriceListTest(TestCase):
    @pytest.mark.back_end_tests
    def test_price_list_unique_name_per_workspace(self):
        price_list = StandardPriceListFactory.create(name="Wholesale")
        # Bypass the factory's `django_get_or_create` (which would just
        # return the existing row) to actually exercise the DB constraint.
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                PriceList.objects.create(workspace=price_list.workspace, name="Wholesale")

    @pytest.mark.back_end_tests
    def test_product_price_without_price_list_is_workspace_default(self):
        variant = StandardProductVariantFactory.create()
        price = StandardPriceFactory.create(variant=variant, price_list=None)
        self.assertIsNone(price.price_list)


class PriceResolutionPrecedenceTest(TestCase):
    """ADR-0005 §Drei-Ebenen-Preisvorrang / REQ-0012 AC-2."""

    def setUp(self):
        self.workspace = DefaultWorkspaceFactory()
        self.unit = StandardUnitFactory.create()
        self.currency = StandardCurrencyFactory.create()
        self.product = StandardProductTypeFactory.create()
        self.variant = StandardProductVariantFactory.create(product=self.product, sku="SKU-PRECEDENCE")
        self.price_list = StandardPriceListFactory.create(name="Channel Webshop")

    @pytest.mark.back_end_tests
    def test_price_list_price_takes_precedence_over_default(self):
        StandardPriceFactory.create(
            variant=self.variant, price="100.00", unit=self.unit, currency=self.currency,
            party_group=None, valid_from=None, valid_until=None, price_list=None,
        )
        StandardPriceFactory.create(
            variant=self.variant, price="80.00", unit=self.unit, currency=self.currency,
            party_group=None, valid_from=None, valid_until=None, price_list=self.price_list,
        )
        result = resolve_price(
            self.variant, datetime.date(2024, 1, 1), self.unit, None, self.currency,
            price_list=self.price_list,
        )
        self.assertEqual(str(result), "80.00")

    @pytest.mark.back_end_tests
    def test_falls_back_to_workspace_default_when_no_price_list_match(self):
        StandardPriceFactory.create(
            variant=self.variant, price="100.00", unit=self.unit, currency=self.currency,
            party_group=None, valid_from=None, valid_until=None, price_list=None,
        )
        result = resolve_price(
            self.variant, datetime.date(2024, 1, 1), self.unit, None, self.currency,
            price_list=self.price_list,
        )
        self.assertEqual(str(result), "100.00")

    @pytest.mark.back_end_tests
    def test_customer_group_transform_applies_on_top_of_resolved_price(self):
        base_group = StandardCustomerGroupFactory.create()
        target_group = StandardCustomerGroupFactory.create(name="VIP")
        StandardPriceFactory.create(
            variant=self.variant, price="100.00", unit=self.unit, currency=self.currency,
            party_group=base_group, valid_from=None, valid_until=None, price_list=None,
        )
        StandardCustomerGroupTransformFactory.create(
            from_party_group=base_group,
            to_party_group=target_group,
            product_type=self.product,
            factor="0.5",
        )
        from tests.factories.contacts.customer_factory import StandardCustomerFactory

        customer = StandardCustomerFactory.create(is_member_of=(target_group,))
        result = resolve_price(self.variant, datetime.date(2024, 1, 1), self.unit, customer, self.currency)
        self.assertEqual(float(result), 50.0)

    @pytest.mark.back_end_tests
    def test_no_price_found_raises(self):
        with self.assertRaises(NoPriceFound):
            resolve_price(self.variant, datetime.date(2024, 1, 1), self.unit, None, self.currency)
