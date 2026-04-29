# -*- coding: utf-8 -*-
from rest_framework import serializers

from koalixcrm.contracts.models.despatch_advice import DespatchAdvice


class DespatchAdviceJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = DespatchAdvice
        fields = '__all__'
