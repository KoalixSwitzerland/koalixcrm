from rest_framework import serializers

from koalixcrm.crm.reporting.work import Work
from koalixcrm.crm.reporting.human_resource import HumanResource
from koalixcrm.crm.reporting.task import Task
from koalixcrm.crm.reporting.reporting_period import ReportingPeriod
from koalixcrm.crm.rest.human_resource_rest import OptionHumanResourceJSONSerializer
from koalixcrm.crm.rest.reporting_period_rest import OptionReportingPeriodJSONSerializer
from koalixcrm.crm.rest.task_type_rest import OptionTaskJSONSerializer


class OptionWorkJSONSerializer(serializers.HyperlinkedModelSerializer):
    humanResource = OptionHumanResourceJSONSerializer(required=False, read_only=True)
    reportingPeriod = OptionReportingPeriodJSONSerializer(required=False, read_only=True)
    task = OptionTaskJSONSerializer(required=False, read_only=True)
    date = serializers.DateField(source='date')
    startTime = serializers.TimeField(source='start_time')
    stopTime = serializers.TimeField(source='stop_time')
    workedHours = serializers.DecimalField(source='worked_hours')
    shortDescription = serializers.CharField(source='short_description')
    description = serializers.CharField(source='description')

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
    humanResource = OptionHumanResourceJSONSerializer(source='human_resource')
    reportingPeriod = OptionReportingPeriodJSONSerializer(source='reporting_period',)
    task = OptionTaskJSONSerializer(source='task')
    date = serializers.DateField(source='date')
    startTime = serializers.TimeField(source='start_time')
    stopTime = serializers.TimeField(source='stop_time')
    workedHours = serializers.DecimalField(source='worked_hours')
    shortDescription = serializers.CharField(source='short_description')
    description = serializers.CharField(source='description')

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
