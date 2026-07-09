# -*- coding: utf-8 -*-
"""ADR-0004 JSON read-mirror: synchronous consistency with the typed EAV
value tables via `post_save`/`post_delete` signals."""
import pytest
from django.test import TestCase

from koalixcrm.products.models.product_attribute_mirror import ProductAttributeMirror
from koalixcrm.products.tests.factories.attribute_definition_factory import (
    StandardAttributeDefinitionFactory,
)
from koalixcrm.products.tests.factories.product_attribute_value_factories import (
    StandardProductAttributeEnumFactory,
)
from koalixcrm.products.tests.factories.product_type_factory import StandardProductTypeFactory
from koalixcrm.products.tests.factories.product_variant_factory import (
    StandardProductVariantFactory,
)


class AttributeMirrorConsistencyTest(TestCase):
    @pytest.mark.back_end_tests
    def test_mirror_created_on_value_save(self):
        definition = StandardAttributeDefinitionFactory.create(key="mirror-create")
        product = StandardProductTypeFactory.create()
        StandardProductAttributeEnumFactory.create(product=product, attribute_definition=definition, value="matt")

        mirror = ProductAttributeMirror.objects.get(product=product, variant__isnull=True)
        self.assertEqual(mirror.data["mirror-create"]["value"], "matt")
        self.assertEqual(mirror.data["mirror-create"]["source"], "PRODUCT")

    @pytest.mark.back_end_tests
    def test_mirror_updates_on_value_change(self):
        definition = StandardAttributeDefinitionFactory.create(key="mirror-update")
        product = StandardProductTypeFactory.create()
        row = StandardProductAttributeEnumFactory.create(
            product=product, attribute_definition=definition, value="matt"
        )
        row.value = "gloss"
        row.save()

        mirror = ProductAttributeMirror.objects.get(product=product, variant__isnull=True)
        self.assertEqual(mirror.data["mirror-update"]["value"], "gloss")

    @pytest.mark.back_end_tests
    def test_mirror_updates_on_value_delete(self):
        definition = StandardAttributeDefinitionFactory.create(key="mirror-delete")
        product = StandardProductTypeFactory.create()
        row = StandardProductAttributeEnumFactory.create(
            product=product, attribute_definition=definition, value="matt"
        )
        row.delete()

        mirror = ProductAttributeMirror.objects.get(product=product, variant__isnull=True)
        self.assertNotIn("mirror-delete", mirror.data)

    @pytest.mark.back_end_tests
    def test_variant_override_maintains_its_own_mirror_row(self):
        definition = StandardAttributeDefinitionFactory.create(key="mirror-variant")
        product = StandardProductTypeFactory.create()
        variant = StandardProductVariantFactory.create(product=product, sku="SKU-MIRROR")
        StandardProductAttributeEnumFactory.create(
            product=product, variant=None, attribute_definition=definition, value="matt"
        )
        StandardProductAttributeEnumFactory.create(
            product=product, variant=variant, attribute_definition=definition, value="gloss"
        )

        product_mirror = ProductAttributeMirror.objects.get(product=product, variant__isnull=True)
        variant_mirror = ProductAttributeMirror.objects.get(product=product, variant=variant)
        self.assertEqual(product_mirror.data["mirror-variant"]["value"], "matt")
        self.assertEqual(variant_mirror.data["mirror-variant"]["value"], "gloss")
        self.assertEqual(variant_mirror.data["mirror-variant"]["source"], "OVERRIDE")
