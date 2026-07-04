# -*- coding: utf-8 -*-
"""ADR-0003 — `ProductMedia.media_type` knows exactly `image`, `datasheet`
and `certificate`; any other value is rejected by the system. Also covers
the "exactly one of product/variant" invariant from the ADR-0021 keying
table ("both levels", union at read time)."""
import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase

from koalixcrm.products.models.choices import ProductMediaType
from koalixcrm.products.models.product_media import ProductMedia
from tests.factories.products.product_media_factory import StandardProductMediaFactory
from tests.factories.products.product_type_factory import StandardProductTypeFactory
from tests.factories.products.product_variant_factory import (
    StandardProductVariantFactory,
)


class ProductMediaTypeRejectionTest(TestCase):
    @pytest.mark.back_end_tests
    def test_image_is_accepted(self):
        media = StandardProductMediaFactory.create(media_type=ProductMediaType.IMAGE)
        media.full_clean()

    @pytest.mark.back_end_tests
    def test_datasheet_is_accepted(self):
        media = StandardProductMediaFactory.create(media_type=ProductMediaType.DATASHEET)
        media.full_clean()

    @pytest.mark.back_end_tests
    def test_certificate_is_accepted(self):
        media = StandardProductMediaFactory.create(media_type=ProductMediaType.CERTIFICATE)
        media.full_clean()

    @pytest.mark.back_end_tests
    def test_other_media_type_value_is_rejected_at_validation(self):
        product = StandardProductTypeFactory.create()
        media = ProductMedia(
            workspace=product.workspace,
            product=product,
            media_type="video",
            object_key="products/some-video.mp4",
        )
        with self.assertRaises(ValidationError):
            media.full_clean()

    @pytest.mark.back_end_tests
    def test_media_must_reference_exactly_one_of_product_or_variant(self):
        product = StandardProductTypeFactory.create()
        media = ProductMedia(
            workspace=product.workspace,
            product=None,
            variant=None,
            media_type=ProductMediaType.IMAGE,
            object_key="products/orphan.jpg",
        )
        with self.assertRaises(ValidationError):
            media.full_clean()

    @pytest.mark.back_end_tests
    def test_media_cannot_reference_both_product_and_variant(self):
        product = StandardProductTypeFactory.create()
        variant = StandardProductVariantFactory.create(product=product)
        media = ProductMedia(
            workspace=product.workspace,
            product=product,
            variant=variant,
            media_type=ProductMediaType.IMAGE,
            object_key="products/both.jpg",
        )
        with self.assertRaises(ValidationError):
            media.full_clean()

    @pytest.mark.back_end_tests
    def test_database_check_constraint_enforces_exactly_one(self):
        """Belt-and-braces: the DB-level CheckConstraint also rejects rows
        that bypass `clean()` (e.g. bulk_create / raw QuerySet.create())."""
        product = StandardProductTypeFactory.create()
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                ProductMedia.objects.create(
                    workspace=product.workspace,
                    product=None,
                    variant=None,
                    media_type=ProductMediaType.IMAGE,
                    object_key="products/bypassed-clean.jpg",
                )

    @pytest.mark.back_end_tests
    def test_variant_level_media_is_valid(self):
        product = StandardProductTypeFactory.create()
        variant = StandardProductVariantFactory.create(product=product)
        media = ProductMedia(
            workspace=product.workspace,
            product=None,
            variant=variant,
            media_type=ProductMediaType.DATASHEET,
            object_key="products/variant-datasheet.pdf",
        )
        media.full_clean()
        media.save()
        self.assertEqual(variant.media_items.count(), 1)
