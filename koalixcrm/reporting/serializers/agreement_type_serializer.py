from __future__ import annotations

from rest_framework import serializers

from koalixcrm.reporting.models.agreement_type import AgreementType


class OptionAgreementTypeJSONSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    title = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)

    class Meta:
        model = AgreementType
        fields = ('id',
                  'title',
                  'description')


class AgreementTypeJSONSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    description = serializers.CharField()

    class Meta:
        model = AgreementType
        fields = ('id',
                  'title',
                  'description')
