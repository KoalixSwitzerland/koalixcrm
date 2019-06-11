# -*- coding: utf-8 -*-
from rest_framework import serializers
from koalixcrm.crm.reporting.project import Project
from koalixcrm.crm.reporting.reporting_period import ReportingPeriod
from koalixcrm.crm.reporting.reporting_period_status import ReportingPeriodStatus
from koalixcrm.crm.rest.reporting_period_status_rest import OptionReportingPeriodStatusJSONSerializer
from koalixcrm.crm.rest.project_rest import OptionProjectJSONSerializer


class OptionReportingPeriodJSONSerializer(serializers.HyperlinkedModelSerializer):
    project = OptionProjectJSONSerializer(source='project', read_only=True)
    title = serializers.CharField(source='title', read_only=True)
    begin = serializers.DateField(source='begin', read_only=True)
    end = serializers.DateField(source='end', read_only=True)
    status = OptionReportingPeriodStatusJSONSerializer(source='status', read_only=True)

    class Meta:
        model = ReportingPeriod
        fields = ('project',
                  'title',
                  'begin',
                  'end',
                  'status')


class ReportingPeriodJSONSerializer(serializers.HyperlinkedModelSerializer):
    project = OptionProjectJSONSerializer(source='project')
    title = serializers.CharField(source='title')
    begin = serializers.DateField(source='begin')
    end = serializers.DateField(source='end')
    status = OptionReportingPeriodStatusJSONSerializer(source='status')

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



