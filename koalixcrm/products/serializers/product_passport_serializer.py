# -*- coding: utf-8 -*-
from __future__ import annotations

from rest_framework import serializers

from koalixcrm.products.models.product_passport import ProductPassport


class ProductPassportJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPassport
        fields = ('id', 'product', 'passport_data')
