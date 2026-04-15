# -*- coding: utf-8 -*-
from rest_framework import serializers
from koalixcrm.contracts.models.quote import Quote


class QuoteJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = '__all__'
