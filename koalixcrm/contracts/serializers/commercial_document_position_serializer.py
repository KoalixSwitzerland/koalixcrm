# -*- coding: utf-8 -*-
from rest_framework import serializers
from koalixcrm.contracts.models.commercial_document_position import CommercialDocumentPosition


class CommercialDocumentPositionJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommercialDocumentPosition
        fields = '__all__'
