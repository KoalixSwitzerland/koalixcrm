# -*- coding: utf-8 -*-
from __future__ import annotations

from rest_framework import serializers

from koalixcrm.products.models.classification import Classification, ClassificationNode


class ClassificationJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classification
        fields = ('id', 'code', 'name', 'description')


class ClassificationNodeJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassificationNode
        fields = ('id', 'classification', 'parent', 'code', 'name', 'level')
