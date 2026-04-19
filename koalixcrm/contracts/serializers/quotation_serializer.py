# -*- coding: utf-8 -*-
from rest_framework import serializers
from koalixcrm.contracts.models.quotation import Quotation


class QuotationJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quotation
        fields = '__all__'
        read_only_fields = ('workspace',)
