# -*- coding: utf-8 -*-
from rest_framework import serializers
from koalixcrm.products.models.unit_transform import UnitTransform


class UnitTransformJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitTransform
        fields = '__all__'
