# -*- coding: utf-8 -*-
"""Canonical `koalix.*` product attribute vocabulary (ADR-0018).

Business logic must read canonical keys exclusively through
`get_canonical_value` / `CANONICAL_KEYS` — never a classification
standard's native attribute identifier directly. The registry is
intentionally a Python constant (not a DB table): ADR-0018 states the
vocabulary is small, stable, and grows only via an ADR-0018 amendment, not
free operator extension.

Two kinds of canonical key:
  * **column-backed** — read straight off a Layer-1 column (`Product` or
    `ProductVariant`); never touches the EAV layer. e.g.
    `koalix.weight_kg` -> `ProductVariant.weight_kg`,
    `koalix.country_of_origin` -> `Product.country_of_origin`.
  * **eav-backed** — resolved through the ADR-0004 cascade against the
    `AttributeDefinition` whose `canonical_key` matches.
"""
from __future__ import annotations

import datetime
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Callable

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

if TYPE_CHECKING:
    from koalixcrm.products.models.product import Product
    from koalixcrm.products.models.product_attribute_mapping import (
        ProductAttributeMapping,
    )
    from koalixcrm.products.models.product_variant import ProductVariant


@dataclass(frozen=True)
class CanonicalKeySpec:
    key: str
    data_type: str
    source: str  # "column" or "eav"
    column_accessor: Callable[[Product, "ProductVariant | None"], Any] | None = None


def _weight_kg(product: Product, variant: "ProductVariant | None") -> Any:
    return variant.weight_kg if variant is not None else None


def _country_of_origin(product: Product, variant: "ProductVariant | None") -> Any:
    return product.country_of_origin


# ADR-0018 seed table. Two of the nine keys are column-backed (ADR-0003
# Layer-1 fields already exist); the remaining seven are eav-backed and
# require an `AttributeDefinition` with a matching `canonical_key` to carry
# a value (see `koalixcrm/products/fixtures/canonical_attribute_definitions.json`,
# added when an operator wants to set them).
CANONICAL_KEYS: dict[str, CanonicalKeySpec] = {
    "koalix.weight_kg": CanonicalKeySpec("koalix.weight_kg", "decimal", "column", _weight_kg),
    "koalix.country_of_origin": CanonicalKeySpec(
        "koalix.country_of_origin", "string", "column", _country_of_origin
    ),
    "koalix.shelf_life_days": CanonicalKeySpec("koalix.shelf_life_days", "int", "eav"),
    "koalix.storage_temp_min_c": CanonicalKeySpec("koalix.storage_temp_min_c", "decimal", "eav"),
    "koalix.storage_temp_max_c": CanonicalKeySpec("koalix.storage_temp_max_c", "decimal", "eav"),
    "koalix.hazard_class": CanonicalKeySpec("koalix.hazard_class", "enum", "eav"),
    "koalix.is_serialized": CanonicalKeySpec("koalix.is_serialized", "bool", "eav"),
    "koalix.is_lot_tracked": CanonicalKeySpec("koalix.is_lot_tracked", "bool", "eav"),
    "koalix.regulated_substance": CanonicalKeySpec("koalix.regulated_substance", "bool", "eav"),
}


def get_canonical_value(
    canonical_key: str,
    product: Product,
    variant: "ProductVariant | None" = None,
) -> Any:
    """Resolve the effective value of a canonical key for `product`
    (optionally `variant`), applying the ADR-0018 §Quellpriorität rule for
    eav-backed keys (an operator-explicit value always outranks an import;
    among imports, structurally the last-written one wins because the
    typed value row is unique per (product, variant, attribute_definition)
    — see `import_canonical_value`)."""
    spec = CANONICAL_KEYS.get(canonical_key)
    if spec is None:
        raise KeyError(f"Unknown canonical key: {canonical_key!r}")

    if spec.source == "column":
        return spec.column_accessor(product, variant)

    from koalixcrm.products.models.attribute_definition import AttributeDefinition
    from koalixcrm.products.services.attribute_cascade import resolve_attribute_value

    definition = AttributeDefinition.objects.filter(
        canonical_key=canonical_key, workspace=product.workspace
    ).first()
    if definition is None:
        return None
    return resolve_attribute_value(product, definition, variant=variant).value


def import_canonical_value(
    mapping: "ProductAttributeMapping",
    product: Product,
    raw_value: Any,
    variant: "ProductVariant | None" = None,
    imported_at: datetime.datetime | None = None,
) -> None:
    """Write a Layer-3-adapter-imported value for `mapping.canonical_key`
    on `product` (ADR-0018 Mapping-Mechanismus). Refuses to clobber an
    existing operator-explicit value (`imported_at IS NULL`), per the
    ADR-0018 source-priority rule: operator-set values always outrank
    imports, regardless of import recency."""
    from django.utils import timezone

    from koalixcrm.products.models.attribute_definition import AttributeDefinition
    from koalixcrm.products.services.attribute_cascade import _value_model_for

    definition = AttributeDefinition.objects.filter(
        canonical_key=mapping.canonical_key, workspace=product.workspace
    ).first()
    if definition is None:
        raise ValidationError(
            _("No AttributeDefinition backs canonical key %(key)s in this workspace.")
            % {"key": mapping.canonical_key}
        )

    model = _value_model_for(definition.data_type)
    existing = model.objects.filter(product=product, variant=variant, attribute_definition=definition).first()
    if existing is not None and existing.imported_at is None:
        return  # operator-explicit value wins; imports never overwrite it.

    model.objects.update_or_create(
        product=product,
        variant=variant,
        attribute_definition=definition,
        defaults={
            "workspace": product.workspace,
            "value": raw_value,
            "source_mapping": mapping,
            "imported_at": imported_at or timezone.now(),
        },
    )
