# -*- coding: utf-8 -*-
from __future__ import annotations

from rest_framework import serializers

from koalixcrm.products.models.product_media import ProductMedia


class ProductMediaJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductMedia
        fields = ('id', 'product', 'variant', 'media_type', 'object_key')
