from rest_framework import serializers
from koalixcrm.crm.reporting.estimation_status import EstimationStatus


class OptionEstimationStatusJSONSerializer(serializers.HyperlinkedModelSerializer):
    title = serializers.CharField(source='title', read_only=True)
    description = serializers.CharField(source='description', read_only=True)
    isObsolete = serializers.BooleanField(source='is_obsolete', read_only=True)

    class Meta:
        model = EstimationStatus
        fields = ('title',
                  'description',
                  'is_obsolete')


class EstimationStatusJSONSerializer(serializers.HyperlinkedModelSerializer):
    title = serializers.CharField(source='title')
    description = serializers.CharField(source='description')
    isObsolete = serializers.BooleanField(source='is_obsolete')

    class Meta:
        model = EstimationStatus
        fields = ('title',
                  'description',
                  'is_obsolete')
