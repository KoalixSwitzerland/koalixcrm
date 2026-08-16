# -*- coding: utf-8 -*-
from __future__ import annotations

from rest_framework import serializers

from koalixcrm.products.models.product_classification import ProductClassification


class ProductClassificationJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductClassification
        fields = ('id', 'product', 'classification_node', 'date_of_creation')
        read_only_fields = ('date_of_creation',)
