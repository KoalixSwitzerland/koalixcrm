# -*- coding: utf-8 -*-
from __future__ import annotations

from rest_framework import serializers

from koalixcrm.products.models.attribute_set_default import AttributeSetDefault


class AttributeSetDefaultJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeSetDefault
        fields = ('id', 'attribute_set', 'attribute_definition', 'default_value')
