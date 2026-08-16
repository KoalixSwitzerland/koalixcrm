# -*- coding: utf-8 -*-
"""ADR-0004 Amendment 2026-06-28 / ADR-0021: variant-override -> product-
value -> family-/AttributeSet-default cascade resolution."""
import pytest
from django.test import TestCase

from koalixcrm.products.services.attribute_cascade import (
    CascadeSource,
    resolve_attribute_value,
)
from koalixcrm.products.tests.factories.attribute_definition_factory import (
    StandardAttributeDefinitionFactory,
)
from koalixcrm.products.tests.factories.attribute_set_default_factory import (
    StandardAttributeSetDefaultFactory,
)
from koalixcrm.products.tests.factories.attribute_set_factory import StandardAttributeSetFactory
from koalixcrm.products.tests.factories.product_attribute_value_factories import (
    StandardProductAttributeEnumFactory,
)
from koalixcrm.products.tests.factories.product_type_factory import StandardProductTypeFactory
from koalixcrm.products.tests.factories.product_variant_factory import (
    StandardProductVariantFactory,
)


class AttributeCascadeTest(TestCase):
    @pytest.mark.back_end_tests
    def test_no_value_anywhere_resolves_to_none(self):
        product = StandardProductTypeFactory.create()
        definition = StandardAttributeDefinitionFactory.create(key="no-value-anywhere")
        resolved = resolve_attribute_value(product, definition)
        self.assertIsNone(resolved.value)
        self.assertEqual(resolved.source, CascadeSource.NONE)

    @pytest.mark.back_end_tests
    def test_family_default_applies_when_no_product_or_variant_value(self):
        definition = StandardAttributeDefinitionFactory.create(key="gloss-cascade-default")
        product = StandardProductTypeFactory.create()
        attribute_set = StandardAttributeSetFactory.create(
            product_family=None, kind=product.kind, classification_node=None
        )
        StandardAttributeSetDefaultFactory.create(
            attribute_set=attribute_set, attribute_definition=definition, default_value="matt"
        )

        resolved = resolve_attribute_value(product, definition)
        self.assertEqual(resolved.value, "matt")
        self.assertEqual(resolved.source, CascadeSource.DEFAULT)

    @pytest.mark.back_end_tests
    def test_product_value_overrides_default(self):
        definition = StandardAttributeDefinitionFactory.create(key="gloss-cascade-product")
        product = StandardProductTypeFactory.create()
        attribute_set = StandardAttributeSetFactory.create(kind=product.kind)
        StandardAttributeSetDefaultFactory.create(
            attribute_set=attribute_set, attribute_definition=definition, default_value="matt"
        )
        StandardProductAttributeEnumFactory.create(product=product, variant=None, attribute_definition=definition, value="satin")

        resolved = resolve_attribute_value(product, definition)
        self.assertEqual(resolved.value, "satin")
        self.assertEqual(resolved.source, CascadeSource.PRODUCT)

    @pytest.mark.back_end_tests
    def test_variant_override_wins_over_product_value(self):
        definition = StandardAttributeDefinitionFactory.create(key="gloss-cascade-variant")
        product = StandardProductTypeFactory.create()
        variant = StandardProductVariantFactory.create(product=product, sku="SKU-CASCADE")
        StandardProductAttributeEnumFactory.create(product=product, variant=None, attribute_definition=definition, value="satin")
        StandardProductAttributeEnumFactory.create(product=product, variant=variant, attribute_definition=definition, value="gloss")

        resolved_for_variant = resolve_attribute_value(product, definition, variant=variant)
        self.assertEqual(resolved_for_variant.value, "gloss")
        self.assertEqual(resolved_for_variant.source, CascadeSource.OVERRIDE)

        resolved_for_product = resolve_attribute_value(product, definition, variant=None)
        self.assertEqual(resolved_for_product.value, "satin")
        self.assertEqual(resolved_for_product.source, CascadeSource.PRODUCT)

    @pytest.mark.back_end_tests
    def test_variant_without_override_inherits_product_value(self):
        definition = StandardAttributeDefinitionFactory.create(key="gloss-cascade-inherit")
        product = StandardProductTypeFactory.create()
        variant = StandardProductVariantFactory.create(product=product, sku="SKU-INHERIT")
        StandardProductAttributeEnumFactory.create(product=product, variant=None, attribute_definition=definition, value="satin")

        resolved = resolve_attribute_value(product, definition, variant=variant)
        self.assertEqual(resolved.value, "satin")
        self.assertEqual(resolved.source, CascadeSource.PRODUCT)
