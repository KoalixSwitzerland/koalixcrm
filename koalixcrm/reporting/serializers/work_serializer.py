from rest_framework import serializers

from koalixcrm.reporting.models.work import Work
from koalixcrm.reporting.models.human_resource import HumanResource
from koalixcrm.reporting.models.task import Task
from koalixcrm.reporting.models.reporting_period import ReportingPeriod
from koalixcrm.reporting.serializers.human_resource_serializer import OptionHumanResourceJSONSerializer
from koalixcrm.reporting.serializers.reporting_period_serializer import OptionReportingPeriodJSONSerializer
from koalixcrm.reporting.serializers.task_serializer import OptionTaskJSONSerializer


class OptionWorkJSONSerializer(serializers.HyperlinkedModelSerializer):
    human_resource = OptionHumanResourceJSONSerializer(required=False, read_only=True)
    reporting_period = OptionReportingPeriodJSONSerializer(required=False, read_only=True)
    task = OptionTaskJSONSerializer(required=False, read_only=True)
    date = serializers.DateField()
    start_time = serializers.TimeField()
    stop_time = serializers.TimeField()
    worked_hours = serializers.DecimalField(max_digits=10, decimal_places=2)
    short_description = serializers.CharField()
    description = serializers.CharField()

    class Meta:
        model = Work
        fields = ('human_resource',
                  'reporting_period',
                  'task',
                  'date',
                  'start_time',
                  'stop_time',
                  'worked_hours',
                  'short_description',
                  'description',)


class WorkJSONSerializer(serializers.HyperlinkedModelSerializer):
    human_resource = OptionHumanResourceJSONSerializer()
    reporting_period = OptionReportingPeriodJSONSerializer()
    task = OptionTaskJSONSerializer()
    date = serializers.DateField()
    start_time = serializers.TimeField()
    stop_time = serializers.TimeField()
    worked_hours = serializers.DecimalField(max_digits=10, decimal_places=2)
    short_description = serializers.CharField()
    description = serializers.CharField()

    class Meta:
        model = Work
        fields = ('human_resource',
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
                work.resource_type = HumanResource.objects.get(id=human_resource.get('id', None))
            else:
                work.resource_type = None
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

    def update(self, work, validated_data):
        # Deserialize human_resource
        human_resource = validated_data.pop('human_resource')
        if human_resource:
            if human_resource.get('id', work.resource_type):
                work.human_resource = HumanResource.objects.get(id=human_resource.get('id', None))
            else:
                work.human_resource = work.human_resource_id
        else:
            work.human_resource = None
        # Deserialize reporting_period
        reporting_period = validated_data.pop('reporting_period')
        if reporting_period:
            if reporting_period.get('id', work.resource_type):
                work.reporting_period = ReportingPeriod.objects.get(id=reporting_period.get('id', None))
            else:
                work.reporting_period = work.reporting_period_id
        else:
            work.reporting_period = None
        # Deserialize task
        task = validated_data.pop('task')
        if task:
            if task.get('id', work.task):
                work.task = Task.objects.get(id=task.get('id', None))
            else:
                work.task = work.task_id
        else:
            work.task = None
