from rest_framework import serializers

from koalixcrm.reporting.models.work import Work
from koalixcrm.reporting.models.human_resource import HumanResource
from koalixcrm.reporting.models.task import Task
from koalixcrm.reporting.models.reporting_period import ReportingPeriod
from koalixcrm.reporting.serializers.human_resource_serializer import OptionHumanResourceJSONSerializer
from koalixcrm.reporting.serializers.reporting_period_serializer import OptionReportingPeriodJSONSerializer
from koalixcrm.reporting.serializers.task_serializer import OptionTaskJSONSerializer


class OptionWorkJSONSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    human_resource = OptionHumanResourceJSONSerializer(required=False, read_only=True)
    reporting_period = OptionReportingPeriodJSONSerializer(required=False, read_only=True)
    task = OptionTaskJSONSerializer(required=False, read_only=True)
    date = serializers.DateField(required=False)
    start_time = serializers.TimeField(required=False)
    stop_time = serializers.TimeField(required=False)
    worked_hours = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    short_description = serializers.CharField(required=False)
    description = serializers.CharField(required=False)

    class Meta:
        model = Work
        fields = ('id',
                  'human_resource',
                  'reporting_period',
                  'task',
                  'date',
                  'start_time',
                  'stop_time',
                  'worked_hours',
                  'short_description',
                  'description',)


class WorkJSONSerializer(serializers.ModelSerializer):
    human_resource = OptionHumanResourceJSONSerializer()
    reporting_period = OptionReportingPeriodJSONSerializer()
    task = OptionTaskJSONSerializer()
    date = serializers.DateField()
    start_time = serializers.TimeField(allow_null=True, required=False)
    stop_time = serializers.TimeField(allow_null=True, required=False)
    worked_hours = serializers.DecimalField(max_digits=10, decimal_places=2)
    short_description = serializers.CharField()
    description = serializers.CharField()

    class Meta:
        model = Work
        fields = ('id',
                  'human_resource',
                  'reporting_period',
                  'task',
                  'date',
                  'start_time',
                  'stop_time',
                  'worked_hours',
                  'short_description',
                  'description',)

    def create(self, validated_data):
        work = Work()
        # Deserialize human_resource
        human_resource = validated_data.pop('human_resource')
        if human_resource:
            if human_resource.get('id', None):
                work.human_resource = HumanResource.objects.get(id=human_resource.get('id', None))
            else:
                work.human_resource = None
        # Deserialize reporting_period
        reporting_period = validated_data.pop('reporting_period')
        if reporting_period:
            if reporting_period.get('id', None):
                work.reporting_period = ReportingPeriod.objects.get(id=reporting_period.get('id', None))
            else:
                work.reporting_period = None
        # Deserialize task
        task = validated_data.pop('task')
        if task:
            if task.get('id', None):
                work.task = Task.objects.get(id=task.get('id', None))
            else:
                work.task = None
        work.date = validated_data.get('date')
        work.start_time = validated_data.get('start_time')
        work.stop_time = validated_data.get('stop_time')
        work.worked_hours = validated_data.get('worked_hours')
        work.short_description = validated_data.get('short_description')
        work.description = validated_data.get('description')
        work.save()
        return work

    def update(self, work, validated_data):
        # Deserialize human_resource
        human_resource = validated_data.pop('human_resource')
        if human_resource:
            if human_resource.get('id', None):
                work.human_resource = HumanResource.objects.get(id=human_resource.get('id', None))
            else:
                work.human_resource = work.human_resource_id
        else:
            work.human_resource = None
        # Deserialize reporting_period
        reporting_period = validated_data.pop('reporting_period')
        if reporting_period:
            if reporting_period.get('id', None):
                work.reporting_period = ReportingPeriod.objects.get(id=reporting_period.get('id', None))
            else:
                work.reporting_period = work.reporting_period_id
        else:
            work.reporting_period = None
        # Deserialize task
        task = validated_data.pop('task')
        if task:
            if task.get('id', None):
                work.task = Task.objects.get(id=task.get('id', None))
            else:
                work.task = work.task_id
        else:
            work.task = None
        work.date = validated_data.get('date', work.date)
        work.start_time = validated_data.get('start_time', work.start_time)
        work.stop_time = validated_data.get('stop_time', work.stop_time)
        work.worked_hours = validated_data.get('worked_hours', work.worked_hours)
        work.short_description = validated_data.get('short_description', work.short_description)
        work.description = validated_data.get('description', work.description)
        work.save()
        return work
