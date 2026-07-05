# -*- coding: utf-8 -*-
"""Shared declarative attribute-validation evaluator (ADR-0020). Pure,
side-effect-free function over serializable rule data and a resolved
attribute-value dict — the same shape a TypeScript port would consume, and
the conformance-test seam ADR-0020 requires (see
`tests/products/fixtures/attribute_rule_conformance.json` and
`tests/products/test_attribute_rule_engine.py`).

Rule shape (`AttributeValidationRule.condition` / `.then`):
    condition: {"attribute": <key>, "op": <op>, "value": <any>}
    then:      {"attribute": <key>, "requirement": "required" | "forbidden"}
             | {"attributes": [<key>, ...], "requirement":
                "mutually_exclusive" | "at_least_one"}

Supported condition operators: eq, neq, in, not_in, exists, not_exists.
This is a deliberately small, pragmatic seed grammar scoped to the
ADR-0004/0018/0019 use cases; ADR-0020 itself defers the concrete grammar
to a follow-up ADR — escalate to `dev-kxcrm-architect` before extending
the operator set.

Justification: framework — pure evaluator invoked synchronously inside attribute_validation's enforcement hook, which runs inside the same clean()/write cycle as the EAV row it validates; still needed with the microservice fleet deleted.
"""
from __future__ import annotations

from typing import Any

_MISSING = object()


def _get(values: dict[str, Any], key: str) -> Any:
    return values.get(key, _MISSING)


def _condition_holds(condition: dict[str, Any], values: dict[str, Any]) -> bool:
    attribute = condition["attribute"]
    op = condition["op"]
    actual = _get(values, attribute)

    if op == "exists":
        return actual is not _MISSING and actual is not None
    if op == "not_exists":
        return actual is _MISSING or actual is None
    if actual is _MISSING:
        actual = None
    if op == "eq":
        return actual == condition.get("value")
    if op == "neq":
        return actual != condition.get("value")
    if op == "in":
        return actual in condition.get("value", [])
    if op == "not_in":
        return actual not in condition.get("value", [])
    raise ValueError(f"Unsupported condition operator: {op!r}")


def _evaluate_then(then: dict[str, Any], values: dict[str, Any]) -> list[str]:
    requirement = then["requirement"]
    violations: list[str] = []

    if requirement == "required":
        attribute = then["attribute"]
        actual = _get(values, attribute)
        if actual is _MISSING or actual is None:
            violations.append(attribute)
    elif requirement == "forbidden":
        attribute = then["attribute"]
        actual = _get(values, attribute)
        if actual is not _MISSING and actual is not None:
            violations.append(attribute)
    elif requirement == "mutually_exclusive":
        attributes = then["attributes"]
        present = [a for a in attributes if _get(values, a) not in (_MISSING, None)]
        if len(present) > 1:
            violations.extend(present)
    elif requirement == "at_least_one":
        attributes = then["attributes"]
        present = [a for a in attributes if _get(values, a) not in (_MISSING, None)]
        if not present:
            violations.extend(attributes)
    else:
        raise ValueError(f"Unsupported requirement: {requirement!r}")
    return violations


def evaluate_rule(rule: dict[str, Any], values: dict[str, Any]) -> dict[str, Any] | None:
    """Evaluate a single serialized rule ({"condition": ..., "then": ...})
    against a flat attribute-key -> value dict. Returns a violation
    payload dict if the rule is violated, else `None`."""
    condition = rule["condition"]
    then = rule["then"]
    if not _condition_holds(condition, values):
        return None
    violated_attributes = _evaluate_then(then, values)
    if not violated_attributes:
        return None
    return {
        "rule_key": rule.get("key"),
        "requirement": then["requirement"],
        "attributes": violated_attributes,
    }


def evaluate_rules(rules: list[dict[str, Any]], values: dict[str, Any]) -> list[dict[str, Any]]:
    """Evaluate a list of serialized rules against `values`. Returns the
    list of violation payloads (empty if `values` conforms to every rule).
    """
    violations = []
    for rule in rules:
        violation = evaluate_rule(rule, values)
        if violation is not None:
            violations.append(violation)
    return violations


def serialize_rule(rule) -> dict[str, Any]:
    """Serialize an `AttributeValidationRule` instance to the plain-dict
    shape `evaluate_rules` (and the DRF endpoint) consume."""
    return {
        "key": rule.key,
        "name": rule.name,
        "order": rule.order,
        "condition": rule.condition,
        "then": rule.then,
    }
