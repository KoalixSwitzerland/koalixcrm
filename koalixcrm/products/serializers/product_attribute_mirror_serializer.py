# -*- coding: utf-8 -*-
"""Read-only serializer for `ProductAttributeMirror` — the mirror is
system-maintained via signals (ADR-0004), never written through the API."""
from __future__ import annotations

from rest_framework import serializers

from koalixcrm.products.models.product_attribute_mirror import ProductAttributeMirror


class ProductAttributeMirrorJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttributeMirror
        fields = ('id', 'product', 'variant', 'data', 'last_modification')
        read_only_fields = fields
