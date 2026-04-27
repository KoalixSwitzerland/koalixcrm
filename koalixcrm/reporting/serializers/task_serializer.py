# -*- coding: utf-8 -*-
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from koalixcrm.reporting.models.project import Project
from koalixcrm.reporting.models.task import Task
from koalixcrm.reporting.models.task_status import TaskStatus
from koalixcrm.reporting.serializers.project_serializer import (
    OptionProjectJSONSerializer,
)
from koalixcrm.reporting.serializers.task_status_serializer import (
    OptionTaskStatusJSONSerializer,
)


class OptionTaskJSONSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    project = OptionProjectJSONSerializer(allow_null=False, read_only=True)
    status = OptionTaskStatusJSONSerializer(allow_null=False, read_only=True)
    last_status_change = serializers.DateField(read_only=True)
    is_reporting_allowed = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ('id',
                  'title',
                  'project',
                  'description',
                  'status',
                  'last_status_change',
                  'is_reporting_allowed',)

    @extend_schema_field(str)
    def get_is_reporting_allowed(self, obj):
        if obj.is_reporting_allowed():
            return "True"
        else:
            return "False"


class TaskJSONSerializer(serializers.ModelSerializer):
    project = OptionProjectJSONSerializer(allow_null=False)
    status = OptionTaskStatusJSONSerializer(allow_null=False)
    last_status_change = serializers.DateField()
    is_reporting_allowed = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ('id',
                  'title',
                  'project',
                  'description',
                  'status',
                  'last_status_change',
                  'is_reporting_allowed',)

    @extend_schema_field(str)
    def get_is_reporting_allowed(self, obj):
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
        task.last_status_change = validated_data['last_status_change']
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
        task.last_status_change = validated_data['last_status_change']
        task.save()
        return task
