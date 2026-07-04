# -*- coding: utf-8 -*-
"""ADR-0020 shared declarative attribute validation: the Python evaluator
against the conformance fixture (`fixtures/attribute_rule_conformance.json`)
that a TypeScript port must also satisfy bit-for-bit (ADR-0020's dual-
evaluator conformance requirement)."""
import json
import os

import pytest
from django.test import SimpleTestCase

from koalixcrm.products.services.attribute_rule_engine import evaluate_rule, evaluate_rules

FIXTURE_PATH = os.path.join(os.path.dirname(__file__), "fixtures", "attribute_rule_conformance.json")


def _load_fixture():
    with open(FIXTURE_PATH) as handle:
        return json.load(handle)


class AttributeRuleConformanceFixtureTest(SimpleTestCase):
    @pytest.mark.back_end_tests
    def test_conformance_fixture_cases(self):
        fixture = _load_fixture()
        self.assertGreaterEqual(len(fixture), 4)
        for entry in fixture:
            rule = entry["rule"]
            for case in entry["cases"]:
                violation = evaluate_rule(rule, case["values"])
                is_violated = violation is not None
                self.assertEqual(
                    is_violated,
                    case["expect_violation"],
                    msg=f"{entry['description']}: {case}",
                )


class AttributeRuleEngineUnitTest(SimpleTestCase):
    @pytest.mark.back_end_tests
    def test_evaluate_rules_accepts_conforming_values(self):
        rules = [{"condition": {"attribute": "a", "op": "eq", "value": 1}, "then": {"attribute": "b", "requirement": "required"}}]
        violations = evaluate_rules(rules, {"a": 1, "b": "present"})
        self.assertEqual(violations, [])

    @pytest.mark.back_end_tests
    def test_evaluate_rules_rejects_violating_values(self):
        rules = [{"condition": {"attribute": "a", "op": "eq", "value": 1}, "then": {"attribute": "b", "requirement": "required"}}]
        violations = evaluate_rules(rules, {"a": 1})
        self.assertEqual(len(violations), 1)
        self.assertEqual(violations[0]["attributes"], ["b"])

    @pytest.mark.back_end_tests
    def test_condition_not_holding_never_violates(self):
        rules = [{"condition": {"attribute": "a", "op": "eq", "value": 1}, "then": {"attribute": "b", "requirement": "required"}}]
        violations = evaluate_rules(rules, {"a": 2})
        self.assertEqual(violations, [])

    @pytest.mark.back_end_tests
    def test_unsupported_operator_raises(self):
        rules = [{"condition": {"attribute": "a", "op": "bogus"}, "then": {"attribute": "b", "requirement": "required"}}]
        with self.assertRaises(ValueError):
            evaluate_rules(rules, {"a": 1})
