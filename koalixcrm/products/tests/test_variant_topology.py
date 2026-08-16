# -*- coding: utf-8 -*-
"""ADR-0021 §3-Ebenen-Topologie / Schlüsselungstabelle — UC-0011.

`ProductVariant` carries the FK to `Product` (not `ProductFamily`); a
`Product` must be creatable with >= 1 variant; `ProductFamily` groups
`Product` objects, not variants; sku/gtin/mpn/weight/dimensions live on
`ProductVariant`.
"""
import pytest
from django.test import TestCase

from koalixcrm.products.models.product_variant import ProductVariant
from koalixcrm.products.tests.factories.product_family_factory import (
    StandardProductFamilyFactory,
)
from koalixcrm.products.tests.factories.product_type_factory import StandardProductTypeFactory
from koalixcrm.products.tests.factories.product_variant_factory import (
    StandardProductVariantFactory,
)


class VariantTopologyTest(TestCase):
    @pytest.mark.back_end_tests
    def test_product_creatable_with_at_least_one_variant(self):
        product = StandardProductTypeFactory.create()
        variant = StandardProductVariantFactory.create(product=product, sku="SKU-A")
        self.assertEqual(product.variants.count(), 1)
        self.assertEqual(variant.product_id, product.id)

    @pytest.mark.back_end_tests
    def test_product_can_have_multiple_variants(self):
        product = StandardProductTypeFactory.create()
        StandardProductVariantFactory.create(product=product, sku="SKU-250G")
        StandardProductVariantFactory.create(product=product, sku="SKU-500G")
        StandardProductVariantFactory.create(product=product, sku="SKU-1KG")
        self.assertEqual(product.variants.count(), 3)

    @pytest.mark.back_end_tests
    def test_variant_fk_points_at_product_not_family(self):
        """ADR-0021 Korrektur 2: ProductVariant FK -> Product."""
        field = ProductVariant._meta.get_field("product")
        self.assertEqual(field.related_model.__name__, "Product")
        self.assertFalse(hasattr(ProductVariant, "product_family"))

    @pytest.mark.back_end_tests
    def test_variant_carries_trade_and_logistics_fields(self):
        """ADR-0021 keying table: sku/gtin/mpn/weight_kg/dimensions_* live
        on ProductVariant, not on Product."""
        variant = StandardProductVariantFactory.create(
            sku="SKU-KEYING",
            gtin="09506000134352",
            mpn="MPN-KEYING",
            weight_kg="2.5000",
            dimensions_length_m="0.3000",
            dimensions_width_m="0.2000",
            dimensions_height_m="0.1000",
        )
        variant.refresh_from_db()
        self.assertEqual(variant.sku, "SKU-KEYING")
        self.assertEqual(variant.gtin, "09506000134352")
        self.assertEqual(variant.mpn, "MPN-KEYING")
        self.assertEqual(str(variant.weight_kg), "2.5000")

        product = variant.product
        self.assertFalse(hasattr(product, "sku"))
        self.assertFalse(hasattr(product, "gtin"))
        self.assertFalse(hasattr(product, "weight_kg"))

    @pytest.mark.back_end_tests
    def test_product_without_family_is_valid(self):
        product = StandardProductTypeFactory.create(product_family=None)
        self.assertIsNone(product.product_family)

    @pytest.mark.back_end_tests
    def test_product_family_groups_products_not_variants(self):
        """ADR-0021 Korrektur 1: ProductFamily groups Product, not
        ProductVariant."""
        family = StandardProductFamilyFactory.create()
        product_a = StandardProductTypeFactory.create(
            product_type_identifier="FAM-A", product_family=family
        )
        product_b = StandardProductTypeFactory.create(
            product_type_identifier="FAM-B", product_family=family
        )
        self.assertEqual(set(family.products.all()), {product_a, product_b})
        self.assertFalse(hasattr(family, "variants"))
