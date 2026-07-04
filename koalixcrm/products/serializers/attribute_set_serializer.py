# -*- coding: utf-8 -*-
from __future__ import annotations

from rest_framework import serializers

from koalixcrm.products.models.attribute_set import AttributeSet, AttributeSetGroup


class AttributeSetJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeSet
        fields = (
            'id', 'name', 'description', 'classification_node', 'kind',
            'product_family', 'attribute_groups',
        )


class AttributeSetGroupJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeSetGroup
        fields = ('id', 'attribute_set', 'attribute_group', 'order')
