from rest_framework import serializers
from koalixcrm.crm.reporting.task_status import TaskStatus


class OptionTaskStatusJSONSerializer(serializers.HyperlinkedModelSerializer):
    title = serializers.CharField(source='title', read_only=True)
    description = serializers.CharField(source='description', read_only=True)
    isDone = serializers.BooleanField(source='is_done', read_only=True)

    class Meta:
        model = TaskStatus
        fields = ('title',
                  'description',
                  'is_done')


class TaskStatusJSONSerializer(serializers.HyperlinkedModelSerializer):
    title = serializers.CharField(source='title')
    description = serializers.CharField(source='description')
    isDone = serializers.BooleanField(source='is_done')

    class Meta:
        model = TaskStatus
        fields = ('title',
                  'description',
                  'is_done')
