# -*- coding: utf-8 -*-
"""Backend enforcement hook for ADR-0020 declarative attribute validation
rules. Call `enforce_attribute_rules()` after writing a typed EAV value row
(see `tests/products/test_attribute_validation_rules.py` for the write-path
usage pattern) to re-validate the product/variant's full effective
attribute-value set against every active `AttributeValidationRule` bound
through its applicable `AttributeSet`s.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils.translation import gettext as _

from koalixcrm.products.services.attribute_rule_engine import evaluate_rules, serialize_rule

if TYPE_CHECKING:
    from koalixcrm.products.models.product import Product
    from koalixcrm.products.models.product_variant import ProductVariant


def _applicable_attribute_sets(product: "Product"):
    from koalixcrm.products.models.attribute_set import AttributeSet

    q = Q(kind=product.kind)
    if product.product_family_id is not None:
        q |= Q(product_family_id=product.product_family_id)
    node_ids = list(product.classifications.values_list("classification_node_id", flat=True))
    if node_ids:
        q |= Q(classification_node_id__in=node_ids)
    return AttributeSet.objects.filter(workspace=product.workspace).filter(q)


def get_effective_values(product: "Product", variant: "ProductVariant | None" = None) -> dict:
    """Cascade-resolved key -> value dict for every attribute definition
    applicable to `product` (via its bound `AttributeSet`s or any existing
    value row)."""
    from koalixcrm.products.models.attribute_definition import AttributeDefinition
    from koalixcrm.products.services.attribute_cascade import resolve_attribute_value
    from koalixcrm.products.services.attribute_mirror import _applicable_attribute_definition_ids

    ids = _applicable_attribute_definition_ids(product)
    values = {}
    for definition in AttributeDefinition.objects.filter(id__in=ids):
        resolved = resolve_attribute_value(product, definition, variant=variant)
        values[definition.key] = resolved.value
    return values


def enforce_attribute_rules(product: "Product", variant: "ProductVariant | None" = None) -> None:
    """Raise `ValidationError` if the effective attribute-value set for
    (product, variant) violates any active `AttributeValidationRule` bound
    through an applicable `AttributeSet`."""
    from koalixcrm.products.models.attribute_validation_rule import AttributeValidationRule

    attribute_sets = _applicable_attribute_sets(product)
    rules = AttributeValidationRule.objects.filter(attribute_set__in=attribute_sets, is_active=True)
    if not rules.exists():
        return

    values = get_effective_values(product, variant=variant)
    serialized = [serialize_rule(rule) for rule in rules]
    violations = evaluate_rules(serialized, values)
    if violations:
        raise ValidationError(
            _("Attribute validation rule violations: %(violations)s") % {"violations": violations}
        )
