# -*- coding: utf-8 -*-
"""`ProductKindPolicy` — the single authoritative `kind`-gating and
kind-immutability component (ADR-0019). Consolidates the scattered
"the application layer must enforce this" caveats from ADR-0006,
ADR-0007, ADR-0009 and ADR-0014 into one place.

Stage 3 (`ServiceProfile`, `BillOfMaterials`, `ProductionOrder`) and the
stock app (`OnHandRecord`, `StockMovement`, `SerialUnit`, `Batch`) do not
exist in this codebase yet. `GATING_MATRIX` is still the complete,
authoritative reference table from ADR-0019 — later stages consult
`check_gate()`/`is_kind_locked()` instead of inventing their own kind
checks. `register_lock_provider()` is the extension seam later stages use
to add their own lock-set membership tests (e.g. "does a BillOfMaterials
exist for this product") without this module knowing about their models.

Justification: framework — lock-provider callbacks perform direct .objects.filter().exists() checks, categorically forbidden to a microservice by ADR-0002 §1.3; consulted inline from Product.clean()/admin/serializers; still needed with the microservice fleet deleted.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from koalixcrm.products.models.choices import ProductKind

if TYPE_CHECKING:
    from koalixcrm.products.models.product import Product

ALLOWED = "ALLOWED"
FORBIDDEN = "FORBIDDEN"
NOT_EVALUATED = "NOT_EVALUATED"

# ADR-0019 Gating-Matrix. "kind-agnostic" dependents (ProductVariant,
# ProductFamily, ProductTranslation, ProductMedia, classification/
# attributes, pricing, ProductSupply, ProductPassport) are deliberately
# absent: ProductKindPolicy does not gate them at all (ADR-0019
# Erläuterungen).
GATING_MATRIX: dict[str, dict[str, str]] = {
    "ServiceProfile": {
        ProductKind.SERVICE: ALLOWED,
        ProductKind.TRADING_GOOD: FORBIDDEN,
        ProductKind.MANUFACTURED_GOOD: FORBIDDEN,
        ProductKind.KIT: FORBIDDEN,
        ProductKind.RAW_MATERIAL: FORBIDDEN,
    },
    "BillOfMaterials": {
        ProductKind.SERVICE: FORBIDDEN,
        ProductKind.TRADING_GOOD: FORBIDDEN,
        ProductKind.MANUFACTURED_GOOD: ALLOWED,
        ProductKind.KIT: ALLOWED,
        ProductKind.RAW_MATERIAL: FORBIDDEN,
    },
    "ProductionOrder": {
        ProductKind.SERVICE: FORBIDDEN,
        ProductKind.TRADING_GOOD: FORBIDDEN,
        ProductKind.MANUFACTURED_GOOD: ALLOWED,
        ProductKind.KIT: ALLOWED,
        ProductKind.RAW_MATERIAL: FORBIDDEN,
    },
    "kit_mode": {
        ProductKind.SERVICE: NOT_EVALUATED,
        ProductKind.TRADING_GOOD: NOT_EVALUATED,
        ProductKind.MANUFACTURED_GOOD: NOT_EVALUATED,
        ProductKind.KIT: ALLOWED,
        ProductKind.RAW_MATERIAL: NOT_EVALUATED,
    },
    "StockFact": {  # OnHandRecord / StockMovement / SerialUnit / Batch
        ProductKind.SERVICE: FORBIDDEN,
        ProductKind.TRADING_GOOD: ALLOWED,
        ProductKind.MANUFACTURED_GOOD: ALLOWED,
        ProductKind.KIT: ALLOWED,
        ProductKind.RAW_MATERIAL: ALLOWED,
    },
}

# tracking_mode is evaluated separately: ADR-0019 says every kind allows
# *some* tracking_mode, but SERVICE allows only NONE.
TRACKING_MODE_NONE = "NONE"


def check_gate(dependent_object_name: str, product_kind: str) -> None:
    """Raise `ValidationError` if `product_kind` does not allow creating
    `dependent_object_name` (a `GATING_MATRIX` key)."""
    row = GATING_MATRIX.get(dependent_object_name)
    if row is None:
        raise KeyError(f"Unknown ProductKindPolicy dependent object: {dependent_object_name!r}")
    verdict = row.get(product_kind, FORBIDDEN)
    if verdict == FORBIDDEN:
        raise ValidationError(
            _("%(dependent)s is not allowed for products of kind %(kind)s.")
            % {"dependent": dependent_object_name, "kind": product_kind}
        )


def check_tracking_mode(product_kind: str, tracking_mode: str) -> None:
    """ADR-0019: `tracking_mode` must be `NONE` for `kind = SERVICE`."""
    if product_kind == ProductKind.SERVICE and tracking_mode != TRACKING_MODE_NONE:
        raise ValidationError(
            _("tracking_mode must be NONE for SERVICE products.")
        )


_LOCK_PROVIDERS: list[Callable[["Product"], bool]] = []


def register_lock_provider(provider: Callable[["Product"], bool]) -> None:
    """Registration seam for later stages: register a callable that
    returns True if `product` has a lock-set member of that stage's own
    (e.g. a `BillOfMaterials` row, a `StockMovement` row)."""
    _LOCK_PROVIDERS.append(provider)


def _kind_bound_attribute_value_exists(product: "Product", kind: str) -> bool:
    """Lock-set member available today: an attribute value under a
    kind-bound `AttributeSet` for this product (ADR-0019 kind-
    Unveränderlichkeit, bullet 6). Checked against `kind` explicitly
    (the persisted kind at the time of the check) rather than
    `product.kind`, since callers may already have assigned a new,
    not-yet-validated kind onto the in-memory instance."""
    from koalixcrm.products.models.attribute_set import AttributeSet
    from koalixcrm.products.services.attribute_cascade import _value_model_for
    from koalixcrm.products.models.choices import AttributeDataType

    kind_bound_sets = AttributeSet.objects.filter(workspace=product.workspace, kind=kind)
    if not kind_bound_sets.exists():
        return False

    from koalixcrm.products.models.attribute_definition import AttributeDefinition

    definition_ids = AttributeDefinition.objects.filter(
        group__attribute_sets__in=kind_bound_sets
    ).values_list("id", flat=True)
    for data_type in AttributeDataType.values:
        try:
            model = _value_model_for(data_type)
        except KeyError:
            continue
        if model.objects.filter(product=product, attribute_definition_id__in=definition_ids).exists():
            return True
    return False


def is_kind_locked(product: "Product", kind: str | None = None) -> bool:
    """True if `kind` may no longer change for `product` (ADR-0019
    kind-Unveränderlichkeit): a lock-set member already exists. `kind`
    defaults to `product.kind`; pass the persisted (old) kind explicitly
    when `product.kind` has already been reassigned in memory."""
    effective_kind = kind if kind is not None else product.kind
    if _kind_bound_attribute_value_exists(product, effective_kind):
        return True
    return any(provider(product) for provider in _LOCK_PROVIDERS)


def validate_kind_change(product: "Product", old_kind: str | None, new_kind: str) -> None:
    """Raise `ValidationError` if `old_kind` (the persisted value, `None`
    for a not-yet-saved product) differs from `new_kind` and the lock-set
    is non-empty."""
    if old_kind is None or old_kind == new_kind:
        return
    if is_kind_locked(product, kind=old_kind):
        raise ValidationError(
            _("kind cannot change: a lock-set member already exists for this product.")
        )
