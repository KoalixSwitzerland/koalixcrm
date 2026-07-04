# -*- coding: utf-8 -*-
"""ADR-0018 canonical `koalix.*` vocabulary: column-backed keys read
straight off Layer-1 columns; eav-backed keys resolve through the
ADR-0004 cascade; import-priority rule (operator-explicit beats import)."""
import pytest
from django.test import TestCase
from django.utils import timezone

from koalixcrm.products.services.canonical_attributes import (
    CANONICAL_KEYS,
    get_canonical_value,
    import_canonical_value,
)
from tests.factories.products.attribute_definition_factory import (
    StandardAttributeDefinitionFactory,
)
from tests.factories.products.product_attribute_mapping_factory import (
    StandardProductAttributeMappingFactory,
)
from tests.factories.products.product_attribute_value_factories import (
    StandardProductAttributeIntFactory,
)
from tests.factories.products.product_type_factory import StandardProductTypeFactory
from tests.factories.products.product_variant_factory import (
    StandardProductVariantFactory,
)


class CanonicalColumnBackedKeyTest(TestCase):
    @pytest.mark.back_end_tests
    def test_weight_kg_reads_from_variant_column(self):
        product = StandardProductTypeFactory.create()
        variant = StandardProductVariantFactory.create(product=product, sku="SKU-CANON", weight_kg="3.4000")
        value = get_canonical_value("koalix.weight_kg", product, variant=variant)
        self.assertEqual(str(value), "3.4000")

    @pytest.mark.back_end_tests
    def test_country_of_origin_reads_from_product_column(self):
        product = StandardProductTypeFactory.create(country_of_origin="CH")
        value = get_canonical_value("koalix.country_of_origin", product)
        self.assertEqual(value, "CH")

    @pytest.mark.back_end_tests
    def test_unknown_canonical_key_raises(self):
        product = StandardProductTypeFactory.create()
        with self.assertRaises(KeyError):
            get_canonical_value("koalix.not_a_real_key", product)

    @pytest.mark.back_end_tests
    def test_seed_table_has_nine_keys(self):
        self.assertEqual(len(CANONICAL_KEYS), 9)


class CanonicalEavBackedKeyTest(TestCase):
    @pytest.mark.back_end_tests
    def test_shelf_life_days_resolves_through_eav_when_backed(self):
        product = StandardProductTypeFactory.create()
        definition = StandardAttributeDefinitionFactory.create(
            key="shelf-life", canonical_key="koalix.shelf_life_days", data_type="int"
        )
        StandardProductAttributeIntFactory.create(product=product, attribute_definition=definition, value=180)

        value = get_canonical_value("koalix.shelf_life_days", product)
        self.assertEqual(value, 180)

    @pytest.mark.back_end_tests
    def test_no_backing_definition_resolves_to_none(self):
        product = StandardProductTypeFactory.create()
        value = get_canonical_value("koalix.shelf_life_days", product)
        self.assertIsNone(value)

    @pytest.mark.back_end_tests
    def test_import_does_not_overwrite_explicit_operator_value(self):
        product = StandardProductTypeFactory.create()
        definition = StandardAttributeDefinitionFactory.create(
            key="shelf-life-priority", canonical_key="koalix.shelf_life_days", data_type="int"
        )
        StandardProductAttributeIntFactory.create(
            product=product, attribute_definition=definition, value=200, imported_at=None
        )
        mapping = StandardProductAttributeMappingFactory.create(canonical_key="koalix.shelf_life_days")

        import_canonical_value(mapping, product, raw_value=999, imported_at=timezone.now())

        value = get_canonical_value("koalix.shelf_life_days", product)
        self.assertEqual(value, 200)

    @pytest.mark.back_end_tests
    def test_import_applies_when_no_explicit_value_exists(self):
        product = StandardProductTypeFactory.create()
        definition = StandardAttributeDefinitionFactory.create(
            key="shelf-life-import", canonical_key="koalix.shelf_life_days", data_type="int"
        )
        mapping = StandardProductAttributeMappingFactory.create(canonical_key="koalix.shelf_life_days")

        import_canonical_value(mapping, product, raw_value=45, imported_at=timezone.now())

        value = get_canonical_value("koalix.shelf_life_days", product)
        self.assertEqual(value, 45)
