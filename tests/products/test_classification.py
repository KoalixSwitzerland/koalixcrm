# -*- coding: utf-8 -*-
"""ADR-0004 classification taxonomy: global tree ops + workspace-scoped
product<->node linkage."""
import pytest
from django.db import IntegrityError, transaction
from django.test import TestCase

from tests.factories.products.classification_factory import (
    StandardClassificationFactory,
    StandardClassificationNodeFactory,
)
from tests.factories.products.product_classification_factory import (
    StandardProductClassificationFactory,
)
from tests.factories.products.product_type_factory import StandardProductTypeFactory


class ClassificationTreeTest(TestCase):
    @pytest.mark.back_end_tests
    def test_node_can_have_parent(self):
        classification = StandardClassificationFactory.create(code="unspsc-tree")
        root = StandardClassificationNodeFactory.create(
            classification=classification, parent=None, code="10", name="Segment"
        )
        child = StandardClassificationNodeFactory.create(
            classification=classification, parent=root, code="10-10", name="Family"
        )
        self.assertEqual(child.parent_id, root.id)
        self.assertIn(child, root.children.all())

    @pytest.mark.back_end_tests
    def test_node_code_unique_per_classification(self):
        classification = StandardClassificationFactory.create(code="unspsc-unique")
        StandardClassificationNodeFactory.create(classification=classification, code="99", name="A")
        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                StandardClassificationNodeFactory.create(classification=classification, code="99", name="B")

    @pytest.mark.back_end_tests
    def test_multiple_classifications_coexist(self):
        unspsc = StandardClassificationFactory.create(code="unspsc-coexist")
        internal = StandardClassificationFactory.create(code="internal-coexist", name="Internal")
        self.assertNotEqual(unspsc.id, internal.id)


class ProductClassificationTest(TestCase):
    @pytest.mark.back_end_tests
    def test_product_can_be_classified_under_multiple_taxonomies(self):
        product = StandardProductTypeFactory.create()
        classification_a = StandardClassificationFactory.create(code="unspsc-multi")
        classification_b = StandardClassificationFactory.create(code="internal-multi", name="Internal")
        node_a = StandardClassificationNodeFactory.create(classification=classification_a, code="a1", name="A1")
        node_b = StandardClassificationNodeFactory.create(classification=classification_b, code="b1", name="B1")

        StandardProductClassificationFactory.create(product=product, classification_node=node_a)
        StandardProductClassificationFactory.create(product=product, classification_node=node_b)

        self.assertEqual(product.classifications.count(), 2)

    @pytest.mark.back_end_tests
    def test_product_classification_unique_per_node(self):
        product = StandardProductTypeFactory.create()
        node = StandardClassificationNodeFactory.create()
        StandardProductClassificationFactory.create(product=product, classification_node=node)
        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                StandardProductClassificationFactory.create(product=product, classification_node=node)
