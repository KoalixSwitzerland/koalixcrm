# -*- coding: utf-8 -*-
from __future__ import annotations

from rest_framework import serializers

from koalixcrm.products.models.product_variant import ProductVariant


class ProductVariantJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ('id',
                  'product',
                  'sku',
                  'gtin',
                  'mpn',
                  'weight_kg',
                  'dimensions_length_m',
                  'dimensions_width_m',
                  'dimensions_height_m',
                  'axis_values',
                  'tracking_mode')
