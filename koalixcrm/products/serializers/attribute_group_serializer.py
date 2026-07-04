# -*- coding: utf-8 -*-
from __future__ import annotations

from rest_framework import serializers

from koalixcrm.products.models.attribute_group import AttributeGroup


class AttributeGroupJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeGroup
        fields = ('id', 'workspace', 'scope', 'key', 'name', 'description')
