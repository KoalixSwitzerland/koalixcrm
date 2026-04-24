# -*- coding: utf-8 -*-
from rest_framework import serializers
from koalixcrm.contracts.models.invoice import Invoice


class InvoiceJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'
        read_only_fields = ('workspace',)
