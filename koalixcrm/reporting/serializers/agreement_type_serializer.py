from rest_framework import serializers
from koalixcrm.reporting.models.agreement_type import AgreementType


class OptionAgreementTypeJSONSerializer(serializers.HyperlinkedModelSerializer):
    title = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)

    class Meta:
        model = AgreementType
        fields = ('title',
                  'description')


class AgreementTypeJSONSerializer(serializers.HyperlinkedModelSerializer):
    title = serializers.CharField()
    description = serializers.CharField()

    class Meta:
        model = AgreementType
        fields = ('title',
                  'description')
