# -*- coding: utf-8 -*-
from rest_framework import serializers
from koalixcrm.contracts.models.sales_document_position import SalesDocumentPosition


class SalesDocumentPositionJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesDocumentPosition
        fields = '__all__'
