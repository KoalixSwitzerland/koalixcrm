# -*- coding: utf-8 -*-
"""Three-step component-`ProductVariant` resolution (ADR-0011/ADR-0014,
Nachtrag 2026-07-04, OQ-0019): used whenever a `BomItem` component needs a
concrete `ProductVariant` at the booking point (production-order component
reservation/picking).

Resolution order:
  1. an explicitly given variant (caller already knows which one);
  2. `BomItem.default_component_variant`, if set;
  3. the component `Product`'s single `ProductVariant`, if it has exactly
     one.

Raises `ComponentVariantResolutionError` (a `ValidationError` subclass) if
none of the three steps yields a variant (e.g. a multi-variant component
Product with no `default_component_variant` and no explicit choice).
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

if TYPE_CHECKING:
    from koalixcrm.products.models.bom_item import BomItem
    from koalixcrm.products.models.product_variant import ProductVariant


class ComponentVariantResolutionError(ValidationError):
    pass


def resolve_component_variant(
    bom_item: "BomItem",
    *,
    explicit_variant: "ProductVariant | None" = None,
) -> "ProductVariant":
    if explicit_variant is not None:
        return explicit_variant

    if bom_item.default_component_variant_id is not None:
        return bom_item.default_component_variant

    from koalixcrm.products.models.product_variant import ProductVariant

    variants = list(ProductVariant.objects.filter(product_id=bom_item.component_product_id)[:2])
    if len(variants) == 1:
        return variants[0]

    raise ComponentVariantResolutionError(
        _("Cannot resolve a ProductVariant for BomItem %(bom_item)s: no explicit variant given, "
          "no default_component_variant set, and the component Product does not have exactly "
          "one ProductVariant.") % {"bom_item": bom_item.pk}
    )
