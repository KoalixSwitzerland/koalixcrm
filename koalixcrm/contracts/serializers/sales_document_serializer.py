# -*- coding: utf-8 -*-
from rest_framework import serializers
from koalixcrm.contracts.models.sales_document import SalesDocument


class SalesDocumentJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesDocument
        fields = '__all__'
