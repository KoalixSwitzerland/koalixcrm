# -*- coding: utf-8 -*-
from rest_framework import serializers
from koalixcrm.products.models.product import Product


class ProductJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
