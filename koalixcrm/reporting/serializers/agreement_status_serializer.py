from rest_framework import serializers
from koalixcrm.reporting.models.agreement_status import AgreementStatus


class OptionAgreementStatusJSONSerializer(serializers.HyperlinkedModelSerializer):
    title = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    is_agreed = serializers.BooleanField(read_only=True)

    class Meta:
        model = AgreementStatus
        fields = ('title',
                  'description',
                  'is_agreed')


class AgreementStatusJSONSerializer(serializers.HyperlinkedModelSerializer):
    title = serializers.CharField()
    description = serializers.CharField()
    is_agreed = serializers.BooleanField()

    class Meta:
        model = AgreementStatus
        fields = ('title',
                  'description',
                  'is_agreed')
