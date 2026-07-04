# -*- coding: utf-8 -*-
"""ADR-0003 §Übersetzungs-Fallback-Kette.

3-step chain: (1) workspace-wide fallback language, (2) first existing
translation ordered by language_code, (3) empty strings — the product
itself is never suppressed.
"""
import pytest
from django.test import TestCase

from koalixcrm.products.services.product_translation_resolver import (
    resolve_product_translation,
)
from tests.factories.products.product_translation_factory import (
    StandardProductTranslationFactory,
)
from tests.factories.products.product_type_factory import StandardProductTypeFactory


class TranslationFallbackChainTest(TestCase):
    @pytest.mark.back_end_tests
    def test_exact_match_wins(self):
        product = StandardProductTypeFactory.create()
        StandardProductTranslationFactory.create(
            product=product, language_code="en", name="English Name"
        )
        StandardProductTranslationFactory.create(
            product=product, language_code="de", name="Deutscher Name"
        )
        resolved = resolve_product_translation(product, "de")
        self.assertEqual(resolved["name"], "Deutscher Name")
        self.assertEqual(resolved["language_code"], "de")

    @pytest.mark.back_end_tests
    def test_step2_first_existing_translation_ordered_by_language_code(self):
        """No exact match, no workspace fallback language configured ->
        first translation ordered by language_code wins."""
        product = StandardProductTypeFactory.create()
        StandardProductTranslationFactory.create(
            product=product, language_code="fr", name="Nom Francais"
        )
        StandardProductTranslationFactory.create(
            product=product, language_code="de", name="Deutscher Name"
        )
        resolved = resolve_product_translation(product, "it")
        # deterministic: "de" sorts before "fr"
        self.assertEqual(resolved["language_code"], "de")
        self.assertEqual(resolved["name"], "Deutscher Name")

    @pytest.mark.back_end_tests
    def test_step3_empty_strings_when_no_translation_exists(self):
        """No translations at all -> empty strings; the product itself is
        not suppressed (the resolver still returns a dict)."""
        product = StandardProductTypeFactory.create()
        resolved = resolve_product_translation(product, "en")
        self.assertEqual(resolved["name"], "")
        self.assertEqual(resolved["short_description"], "")
        self.assertEqual(resolved["long_description"], "")

    @pytest.mark.back_end_tests
    def test_step1_workspace_fallback_language_used_when_configured(self):
        """Step 1: a workspace-configured `default_language` (forward-compat
        attribute; not yet a core.Workspace field in this stage) wins over
        the deterministic step-2 ordering."""
        product = StandardProductTypeFactory.create()
        StandardProductTranslationFactory.create(
            product=product, language_code="fr", name="Nom Francais"
        )
        StandardProductTranslationFactory.create(
            product=product, language_code="de", name="Deutscher Name"
        )
        # Simulate a future core.Workspace.default_language field.
        product.workspace.default_language = "fr"

        resolved = resolve_product_translation(product, "it")
        self.assertEqual(resolved["language_code"], "fr")
        self.assertEqual(resolved["name"], "Nom Francais")
