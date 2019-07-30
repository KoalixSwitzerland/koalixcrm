from rest_framework import serializers
from koalixcrm.crm.reporting.reporting_period_status import ReportingPeriodStatus


class OptionReportingPeriodStatusJSONSerializer(serializers.HyperlinkedModelSerializer):
    title = serializers.CharField(source='title', read_only=True)
    description = serializers.CharField(source='description', read_only=True)
    isDone = serializers.BooleanField(source='is_done', read_only=True)

    class Meta:
        model = ReportingPeriodStatus
        fields = ('title',
                  'description',
                  'is_done')


class ReportingPeriodStatusJSONSerializer(serializers.HyperlinkedModelSerializer):
    title = serializers.CharField(source='title')
    description = serializers.CharField(source='description')
    isDone = serializers.BooleanField(source='is_done')

    class Meta:
        model = ReportingPeriodStatus
        fields = ('title',
                  'description',
                  'is_done')
