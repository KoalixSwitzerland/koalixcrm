from rest_framework import serializers
from koalixcrm.crm.reporting.agreement_status import AgreementStatus


class OptionAgreementStatusJSONSerializer(serializers.HyperlinkedModelSerializer):
    title = serializers.CharField(source='title', read_only=True)
    description = serializers.CharField(source='description', read_only=True)
    isAgreed = serializers.BooleanField(source='is_agreed', read_only=True)

    class Meta:
        model = AgreementStatus
        fields = ('title',
                  'description',
                  'is_agreed')


class AgreementStatusJSONSerializer(serializers.HyperlinkedModelSerializer):
    title = serializers.CharField(source='title')
    description = serializers.CharField(source='description')
    isAgreed = serializers.BooleanField(source='is_agreed')

    class Meta:
        model = AgreementStatus
        fields = ('title',
                  'description',
                  'is_agreed')
