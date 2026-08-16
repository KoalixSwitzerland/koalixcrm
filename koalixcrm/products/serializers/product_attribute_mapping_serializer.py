# -*- coding: utf-8 -*-
from __future__ import annotations

from rest_framework import serializers

from koalixcrm.products.models.product_attribute_mapping import ProductAttributeMapping


class ProductAttributeMappingJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttributeMapping
        fields = ('id', 'source_standard', 'source_attribute_id', 'canonical_key', 'transform')
