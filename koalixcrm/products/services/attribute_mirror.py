# -*- coding: utf-8 -*-
"""Synchronous JSON read-mirror maintenance (ADR-0004). Invoked from
`koalixcrm.products.signals.attribute_mirror` on every typed EAV value
table write/delete; keeps `ProductAttributeMirror` in lock-step with the
source-of-truth typed value tables (no async/eventual-consistency window).
"""
from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from koalixcrm.products.models.attribute_definition import AttributeDefinition
from koalixcrm.products.models.attribute_set import AttributeSet
from koalixcrm.products.models.attribute_set_default import AttributeSetDefault
from koalixcrm.products.models.product_attribute_mirror import ProductAttributeMirror
from koalixcrm.products.services.attribute_cascade import resolve_attribute_value

if TYPE_CHECKING:
    from koalixcrm.products.models.product import Product
    from koalixcrm.products.models.product_variant import ProductVariant

_VALUE_TABLE_NAMES = (
    "productattributestring_values",
    "productattributeint_values",
    "productattributedecimal_values",
    "productattributebool_values",
    "productattributeenum_values",
    "productattributereference_values",
)


def _json_safe(value):
    if isinstance(value, Decimal):
        return str(value)
    return value


def _applicable_attribute_definition_ids(product: Product) -> set[int]:
    ids: set[int] = set()
    for related_name in _VALUE_TABLE_NAMES:
        manager = getattr(product, related_name)
        ids.update(manager.values_list("attribute_definition_id", flat=True))

    from django.db.models import Q

    q = Q(kind=product.kind)
    if product.product_family_id is not None:
        q |= Q(product_family_id=product.product_family_id)
    node_ids = list(product.classifications.values_list("classification_node_id", flat=True))
    if node_ids:
        q |= Q(classification_node_id__in=node_ids)
    candidate_sets = AttributeSet.objects.filter(workspace=product.workspace).filter(q)
    ids.update(
        AttributeSetDefault.objects.filter(attribute_set__in=candidate_sets).values_list(
            "attribute_definition_id", flat=True
        )
    )
    return ids


def rebuild_attribute_mirror(product: Product, variant: ProductVariant | None = None) -> ProductAttributeMirror:
    """Recompute and persist the cascade-resolved JSON mirror for
    (product, variant)."""
    attribute_definition_ids = _applicable_attribute_definition_ids(product)
    definitions = AttributeDefinition.objects.filter(id__in=attribute_definition_ids)

    data: dict = {}
    for definition in definitions:
        resolved = resolve_attribute_value(product, definition, variant=variant)
        key = definition.canonical_key or definition.key
        data[key] = {
            "value": _json_safe(resolved.value),
            "source": resolved.source,
            "attribute_definition_id": definition.id,
        }

    mirror, _created = ProductAttributeMirror.objects.update_or_create(
        product=product,
        variant=variant,
        defaults={"workspace": product.workspace, "data": data},
    )
    return mirror


def rebuild_all_mirrors_for_product(product: Product) -> None:
    """Rebuild the product-level mirror and every variant-level mirror."""
    rebuild_attribute_mirror(product, variant=None)
    for variant in product.variants.all():
        rebuild_attribute_mirror(product, variant=variant)
