from rest_framework import serializers
from koalixcrm.crm.reporting.agreement_type import AgreementType


class OptionAgreementTypeJSONSerializer(serializers.HyperlinkedModelSerializer):
    title = serializers.CharField(source='title', read_only=True)
    description = serializers.CharField(source='description', read_only=True)

    class Meta:
        model = AgreementType
        fields = ('title',
                  'description')


class AgreementTypeJSONSerializer(serializers.HyperlinkedModelSerializer):
    title = serializers.CharField(source='title')
    description = serializers.CharField(source='description')

    class Meta:
        model = AgreementType
        fields = ('title',
                  'description')
