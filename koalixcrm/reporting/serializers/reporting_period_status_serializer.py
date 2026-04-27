from rest_framework import serializers

from koalixcrm.reporting.models.reporting_period_status import ReportingPeriodStatus


class OptionReportingPeriodStatusJSONSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    title = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    is_done = serializers.BooleanField(read_only=True)

    class Meta:
        model = ReportingPeriodStatus
        fields = ('id',
                  'title',
                  'description',
                  'is_done')


class ReportingPeriodStatusJSONSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    description = serializers.CharField()
    is_done = serializers.BooleanField()

    class Meta:
        model = ReportingPeriodStatus
        fields = ('id',
                  'title',
                  'description',
                  'is_done')
