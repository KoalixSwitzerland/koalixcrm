# -*- coding: utf-8 -*-
from rest_framework import serializers
from koalixcrm.contracts.models.commercial_document import CommercialDocument


class CommercialDocumentJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommercialDocument
        fields = '__all__'
