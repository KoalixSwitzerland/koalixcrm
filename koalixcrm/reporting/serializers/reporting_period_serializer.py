# -*- coding: utf-8 -*-
from rest_framework import serializers
from koalixcrm.reporting.models.project import Project
from koalixcrm.reporting.models.reporting_period import ReportingPeriod
from koalixcrm.reporting.models.reporting_period_status import ReportingPeriodStatus
from koalixcrm.reporting.serializers.reporting_period_status_serializer import OptionReportingPeriodStatusJSONSerializer
from koalixcrm.reporting.serializers.project_serializer import OptionProjectJSONSerializer


class OptionReportingPeriodJSONSerializer(serializers.HyperlinkedModelSerializer):
    project = OptionProjectJSONSerializer(read_only=True)
    title = serializers.CharField(read_only=True)
    begin = serializers.DateField(read_only=True)
    end = serializers.DateField(read_only=True)
    status = OptionReportingPeriodStatusJSONSerializer(read_only=True)

    class Meta:
        model = ReportingPeriod
        fields = ('project',
                  'title',
                  'begin',
                  'end',
                  'status')


class ReportingPeriodJSONSerializer(serializers.HyperlinkedModelSerializer):
    project = OptionProjectJSONSerializer()
    title = serializers.CharField()
    begin = serializers.DateField()
    end = serializers.DateField()
    status = OptionReportingPeriodStatusJSONSerializer()

    class Meta:
        model = ReportingPeriod
        fields = ('project',
                  'title',
                  'begin',
                  'end',
                  'status')

    def create(self, validated_data):
        reporting_period = ReportingPeriod()
        # Deserialize project
        project = validated_data.pop('project')
        if project:
            if project.get('id', None):
                reporting_period.project = Project.objects.get(id=project.get('id', None))
            else:
                reporting_period.project = None
        # Deserialize status
        status = validated_data.pop('status')
        if status:
            if status.get('id', None):
                reporting_period.status = ReportingPeriodStatus.objects.get(id=status.get('id', None))
            else:
                reporting_period.status = None
        reporting_period.title = validated_data['title']
        reporting_period.begin = validated_data['begin']
        reporting_period.end = validated_data['end']
        reporting_period.save()
        return reporting_period

    def update(self, reporting_period, validated_data):
        # Deserialize project
        project = validated_data.pop('project')
        if project:
            if project.get('id', reporting_period.project):
                reporting_period.project = Project.objects.get(id=project.get('id', None))
            else:
                reporting_period.project = reporting_period.project_id
        else:
            reporting_period.project = None
        # Deserialize status
        status = validated_data.pop('status')
        if status:
            if status.get('id', reporting_period.status):
                reporting_period.status = ReportingPeriodStatus.objects.get(id=status.get('id', None))
            else:
                reporting_period.status = reporting_period.status_id
        else:
            reporting_period.status = None
        reporting_period.title = validated_data['title']
        reporting_period.begin = validated_data['begin']
        reporting_period.end = validated_data['end']
        reporting_period.save()
        return reporting_period



