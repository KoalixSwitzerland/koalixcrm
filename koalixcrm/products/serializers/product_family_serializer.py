# -*- coding: utf-8 -*-
from __future__ import annotations

from rest_framework import serializers

from koalixcrm.products.models.product_family import ProductFamily


class ProductFamilyJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFamily
        fields = ('id', 'name', 'description')
