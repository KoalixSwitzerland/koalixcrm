# -*- coding: utf-8 -*-
"""Translation fallback chain for `products.Product`.

ADR-0003 §Übersetzungs-Fallback-Kette:
  1. The workspace-wide configured fallback language.
  2. The first existing translation of the product (any language,
     deterministically ordered by `language_code`).
  3. Empty string for all text fields; the product itself is never
     suppressed.

Step 1 reads an optional `default_language` attribute off the product's
workspace. `core.Workspace` does not (yet) carry that field in this stage;
resolution degrades gracefully to step 2 when it is absent, per the ADR's
"the product object itself is never suppressed" guarantee.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from koalixcrm.products.models.product import Product


class ResolvedTranslation(TypedDict):
    language_code: str | None
    name: str
    short_description: str
    long_description: str


def _empty(language_code: str | None = None) -> ResolvedTranslation:
    return {
        "language_code": language_code,
        "name": "",
        "short_description": "",
        "long_description": "",
    }


def resolve_product_translation(product: Product, language_code: str) -> ResolvedTranslation:
    """Resolve the effective translation for `product` in `language_code`
    following the 3-step ADR-0003 fallback chain."""
    translations = list(product.translations.all().order_by("language_code"))

    # Step 0: exact match always wins.
    for translation in translations:
        if translation.language_code == language_code:
            return {
                "language_code": translation.language_code,
                "name": translation.name,
                "short_description": translation.short_description or "",
                "long_description": translation.long_description or "",
            }

    # Step 1: workspace-wide configured fallback language.
    fallback_language = getattr(product.workspace, "default_language", None)
    if fallback_language:
        for translation in translations:
            if translation.language_code == fallback_language:
                return {
                    "language_code": translation.language_code,
                    "name": translation.name,
                    "short_description": translation.short_description or "",
                    "long_description": translation.long_description or "",
                }

    # Step 2: first existing translation, deterministic by language_code.
    if translations:
        translation = translations[0]
        return {
            "language_code": translation.language_code,
            "name": translation.name,
            "short_description": translation.short_description or "",
            "long_description": translation.long_description or "",
        }

    # Step 3: empty strings; the product itself is not suppressed.
    return _empty(language_code)
