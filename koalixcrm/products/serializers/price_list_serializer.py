# -*- coding: utf-8 -*-
from __future__ import annotations

from rest_framework import serializers

from koalixcrm.products.models.price_list import PriceList


class PriceListJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceList
        fields = ('id', 'name', 'channel', 'party_group', 'description')
