# -*- coding: utf-8 -*-
"""ADR-0003 §Lifecycle-Status-Werte — allowed transition rules.

Covers REQ-0005 (documented as a former assumption, now ratified by
ADR-0003). Exercises both the service function directly and
`Product.full_clean()` (the model-level enforcement point).
"""
import pytest
from django.core.exceptions import ValidationError
from django.test import TestCase

from koalixcrm.products.models.choices import ProductLifecycleStatus
from koalixcrm.products.services.product_lifecycle import (
    validate_lifecycle_transition,
)
from koalixcrm.products.tests.factories.product_type_factory import StandardProductTypeFactory


class LifecycleTransitionServiceTest(TestCase):
    """Pure unit tests for `validate_lifecycle_transition` — no DB needed,
    but TestCase is used for consistency with the rest of the suite."""

    @pytest.mark.back_end_tests
    def test_draft_to_active_is_allowed(self):
        validate_lifecycle_transition(ProductLifecycleStatus.DRAFT, ProductLifecycleStatus.ACTIVE)

    @pytest.mark.back_end_tests
    def test_draft_to_external_only_is_allowed(self):
        validate_lifecycle_transition(ProductLifecycleStatus.DRAFT, ProductLifecycleStatus.EXTERNAL_ONLY)

    @pytest.mark.back_end_tests
    def test_active_to_discontinued_is_allowed(self):
        validate_lifecycle_transition(ProductLifecycleStatus.ACTIVE, ProductLifecycleStatus.DISCONTINUED)

    @pytest.mark.back_end_tests
    def test_discontinued_to_archived_is_allowed(self):
        validate_lifecycle_transition(ProductLifecycleStatus.DISCONTINUED, ProductLifecycleStatus.ARCHIVED)

    @pytest.mark.back_end_tests
    def test_no_op_transition_is_allowed(self):
        validate_lifecycle_transition(ProductLifecycleStatus.ACTIVE, ProductLifecycleStatus.ACTIVE)

    @pytest.mark.back_end_tests
    def test_initial_creation_accepts_any_status(self):
        validate_lifecycle_transition(None, ProductLifecycleStatus.EXTERNAL_ONLY)

    @pytest.mark.back_end_tests
    def test_archived_to_active_is_rejected(self):
        with self.assertRaises(ValidationError):
            validate_lifecycle_transition(ProductLifecycleStatus.ARCHIVED, ProductLifecycleStatus.ACTIVE)

    @pytest.mark.back_end_tests
    def test_discontinued_to_draft_is_rejected(self):
        with self.assertRaises(ValidationError):
            validate_lifecycle_transition(ProductLifecycleStatus.DISCONTINUED, ProductLifecycleStatus.DRAFT)

    @pytest.mark.back_end_tests
    def test_external_only_to_anything_else_is_rejected(self):
        for target in (
            ProductLifecycleStatus.DRAFT,
            ProductLifecycleStatus.ACTIVE,
            ProductLifecycleStatus.DISCONTINUED,
            ProductLifecycleStatus.ARCHIVED,
        ):
            with self.assertRaises(ValidationError):
                validate_lifecycle_transition(ProductLifecycleStatus.EXTERNAL_ONLY, target)

    @pytest.mark.back_end_tests
    def test_draft_to_discontinued_is_rejected(self):
        with self.assertRaises(ValidationError):
            validate_lifecycle_transition(ProductLifecycleStatus.DRAFT, ProductLifecycleStatus.DISCONTINUED)


class ProductLifecycleModelCleanTest(TestCase):
    """`Product.clean()` enforces the same rules against the persisted
    lifecycle_status."""

    @pytest.mark.back_end_tests
    def test_illegal_transition_raises_on_full_clean(self):
        product = StandardProductTypeFactory.create(
            lifecycle_status=ProductLifecycleStatus.ARCHIVED,
        )
        product.lifecycle_status = ProductLifecycleStatus.ACTIVE
        with self.assertRaises(ValidationError):
            product.full_clean()

    @pytest.mark.back_end_tests
    def test_legal_transition_passes_full_clean(self):
        product = StandardProductTypeFactory.create(
            lifecycle_status=ProductLifecycleStatus.DRAFT,
        )
        product.lifecycle_status = ProductLifecycleStatus.ACTIVE
        product.full_clean()
