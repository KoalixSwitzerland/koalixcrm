# -*- coding: utf-8 -*-
"""REQ-0022 AC-4 / ADR-0012: FEFO ordering (non-quarantined, ascending
expiry_date nulls-last, tie-break production_date) and FIFO fallback
(ascending received_at); batch_number uniqueness per (workspace, variant)."""
import datetime

import pytest
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from koalixcrm.stock.services.fefo import fefo_order_batches, fifo_order_batches
from tests.factories.products.product_variant_factory import StandardProductVariantFactory
from tests.factories.stock.batch_factory import StandardBatchFactory

TODAY = datetime.date.today()


class FefoOrderingTest(TestCase):
    @pytest.mark.back_end_tests
    def test_fefo_orders_by_ascending_expiry_nulls_last(self):
        variant = StandardProductVariantFactory()
        far = StandardBatchFactory(variant=variant, workspace=variant.workspace,
                                   batch_number="FAR", expiry_date=TODAY + datetime.timedelta(days=90))
        near = StandardBatchFactory(variant=variant, workspace=variant.workspace,
                                    batch_number="NEAR", expiry_date=TODAY + datetime.timedelta(days=10))
        no_expiry = StandardBatchFactory(variant=variant, workspace=variant.workspace,
                                         batch_number="NO-EXPIRY", expiry_date=None)

        ordered = list(fefo_order_batches(variant))
        self.assertEqual(ordered, [near, far, no_expiry])

    @pytest.mark.back_end_tests
    def test_fefo_excludes_quarantined_batches_by_default(self):
        variant = StandardProductVariantFactory()
        ok = StandardBatchFactory(variant=variant, workspace=variant.workspace, batch_number="OK",
                                  expiry_date=TODAY + datetime.timedelta(days=5))
        StandardBatchFactory(variant=variant, workspace=variant.workspace, batch_number="QUARANTINED",
                            expiry_date=TODAY + datetime.timedelta(days=1), quarantine=True)

        ordered = list(fefo_order_batches(variant))
        self.assertEqual(ordered, [ok])

    @pytest.mark.back_end_tests
    def test_fefo_tie_break_by_production_date(self):
        variant = StandardProductVariantFactory()
        older = StandardBatchFactory(variant=variant, workspace=variant.workspace, batch_number="OLDER-PROD",
                                     expiry_date=TODAY + datetime.timedelta(days=20),
                                     production_date=TODAY - datetime.timedelta(days=10))
        newer = StandardBatchFactory(variant=variant, workspace=variant.workspace, batch_number="NEWER-PROD",
                                     expiry_date=TODAY + datetime.timedelta(days=20),
                                     production_date=TODAY - datetime.timedelta(days=1))

        ordered = list(fefo_order_batches(variant))
        self.assertEqual(ordered, [older, newer])

    @pytest.mark.back_end_tests
    def test_fifo_fallback_orders_by_received_at(self):
        variant = StandardProductVariantFactory()
        earlier = StandardBatchFactory(variant=variant, workspace=variant.workspace, batch_number="EARLIER",
                                       expiry_date=None,
                                       received_at=timezone.now() - datetime.timedelta(days=5))
        later = StandardBatchFactory(variant=variant, workspace=variant.workspace, batch_number="LATER",
                                     expiry_date=None, received_at=timezone.now())

        ordered = list(fifo_order_batches(variant))
        self.assertEqual(ordered, [earlier, later])

    @pytest.mark.back_end_tests
    def test_batch_number_unique_per_variant(self):
        variant = StandardProductVariantFactory()
        StandardBatchFactory(variant=variant, workspace=variant.workspace, batch_number="DUP")
        with self.assertRaises(ValidationError):
            StandardBatchFactory.build(variant=variant, workspace=variant.workspace,
                                       batch_number="DUP").full_clean()

    @pytest.mark.back_end_tests
    def test_same_batch_number_allowed_across_variants(self):
        variant_a = StandardProductVariantFactory(sku="SKU-FEFO-A")
        variant_b = StandardProductVariantFactory(sku="SKU-FEFO-B")
        StandardBatchFactory(variant=variant_a, workspace=variant_a.workspace, batch_number="SHARED")
        StandardBatchFactory(variant=variant_b, workspace=variant_b.workspace, batch_number="SHARED")
