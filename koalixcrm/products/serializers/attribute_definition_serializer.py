# -*- coding: utf-8 -*-
from __future__ import annotations

from rest_framework import serializers

from koalixcrm.products.models.attribute_definition import AttributeDefinition


class AttributeDefinitionJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeDefinition
        fields = (
            'id', 'workspace', 'scope', 'key', 'canonical_key', 'label', 'data_type',
            'unit', 'group', 'order', 'min_value', 'max_value', 'regex', 'enum_values',
            'is_localized', 'is_required', 'is_multivalued',
        )
