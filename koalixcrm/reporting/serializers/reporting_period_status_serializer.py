from rest_framework import serializers
from koalixcrm.reporting.models.reporting_period_status import ReportingPeriodStatus


class OptionReportingPeriodStatusJSONSerializer(serializers.HyperlinkedModelSerializer):
    title = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    is_done = serializers.BooleanField(read_only=True)

    class Meta:
        model = ReportingPeriodStatus
        fields = ('title',
                  'description',
                  'is_done')


class ReportingPeriodStatusJSONSerializer(serializers.HyperlinkedModelSerializer):
    title = serializers.CharField()
    description = serializers.CharField()
    is_done = serializers.BooleanField()

    class Meta:
        model = ReportingPeriodStatus
        fields = ('title',
                  'description',
                  'is_done')
