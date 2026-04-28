# -*- coding: utf-8 -*-
from __future__ import annotations

from rest_framework import serializers

from koalixcrm.products.models.product_price import ProductPrice


class ProductPriceJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPrice
        fields = '__all__'
