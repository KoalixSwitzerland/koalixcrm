# -*- coding: utf-8 -*-
"""Read-only serializer for `AttributeValidationRule` — ADR-0020 exposes
the rule payload to the frontend read-only through the REST API; the
backend (Django admin / fixtures / migrations) is the only writer."""
from __future__ import annotations

from rest_framework import serializers

from koalixcrm.products.models.attribute_validation_rule import AttributeValidationRule


class AttributeValidationRuleJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValidationRule
        fields = ('id', 'attribute_set', 'key', 'name', 'order', 'is_active', 'condition', 'then')
        read_only_fields = fields
