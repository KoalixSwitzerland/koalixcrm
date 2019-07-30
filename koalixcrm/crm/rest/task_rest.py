# -*- coding: utf-8 -*-
from rest_framework import serializers
from koalixcrm.crm.reporting.task import Task
from koalixcrm.crm.reporting.project import Project
from koalixcrm.crm.reporting.task_status import TaskStatus
from koalixcrm.crm.rest.project_rest import OptionProjectJSONSerializer
from koalixcrm.crm.rest.task_status_rest import OptionTaskStatusJSONSerializer


class OptionTaskJSONSerializer(serializers.HyperlinkedModelSerializer):
    project = OptionProjectJSONSerializer(allow_null=False, read_only=True)
    status = OptionTaskStatusJSONSerializer(allow_null=False, read_only=True)
    lastStatusChange = serializers.DateField(source='last_status_change', read_only=True)
    isReportingAllowed = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ('id',
                  'title',
                  'project',
                  'description',
                  'status',
                  'lastStatusChange',
                  'isReportingAllowed',)

    def get_isReportingAllowed(self, obj):
        if obj.is_reporting_allowed():
            return "True"
        else:
            return "False"


class TaskJSONSerializer(serializers.HyperlinkedModelSerializer):
    project = OptionProjectJSONSerializer(allow_null=False)
    status = OptionTaskStatusJSONSerializer(allow_null=False)
    lastStatusChange = serializers.DateField(source='last_status_change')
    isReportingAllowed = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ('id',
                  'title',
                  'project',
                  'description',
                  'status',
                  'lastStatusChange',
                  'isReportingAllowed',)

    def get_isReportingAllowed(self, obj):
        if obj.is_reporting_allowed():
            return "True"
        else:
            return "False"

    def create(self, validated_data):
        task = Task()
        # Deserialize project
        project = validated_data.pop('project')
        if project:
            if project.get('id', None):
                task.project = Project.objects.get(id=project.get('id', None))
            else:
                task.project = None
        # Deserialize status
        status = validated_data.pop('status')
        if status:
            if status.get('id', None):
                task.status = TaskStatus.objects.get(id=status.get('id', None))
            else:
                task.status = None
        task.title = validated_data['title']
        task.description = validated_data['description']
        task.last_status_change = validated_data['lastStatusChange']
        task.save()
        return task

    def update(self, task, validated_data):
        # Deserialize project
        project = validated_data.pop('project')
        if project:
            if project.get('id', task.project):
                task.project = Project.objects.get(id=project.get('id', None))
            else:
                task.project = task.project_id
        else:
            task.project = None
        # Deserialize status
        status = validated_data.pop('status')
        if status:
            if status.get('id', task.status):
                task.status = TaskStatus.objects.get(id=status.get('id', None))
            else:
                task.status = task.status_id
        else:
            task.status = None
        task.title = validated_data['title']
        task.description = validated_data['description']
        task.last_status_change = validated_data['lastStatusChange']
        task.save()
        return task



