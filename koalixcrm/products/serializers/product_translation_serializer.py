# -*- coding: utf-8 -*-
from __future__ import annotations

from rest_framework import serializers

from koalixcrm.products.models.product_translation import ProductTranslation


class ProductTranslationJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTranslation
        fields = ('id', 'product', 'language_code', 'name', 'short_description', 'long_description')
