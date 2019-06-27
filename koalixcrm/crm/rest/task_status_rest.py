from rest_framework import serializers
from koalixcrm.crm.reporting.task_status import TaskStatus


class OptionTaskStatusJSONSerializer(serializers.HyperlinkedModelSerializer):
    isDone = serializers.BooleanField(source='is_done', read_only=True)

    class Meta:
        model = TaskStatus
        fields = ('title',
                  'description',
                  'isDone')


class TaskStatusJSONSerializer(serializers.HyperlinkedModelSerializer):
    isDone = serializers.BooleanField(source='is_done')

    class Meta:
        model = TaskStatus
        fields = ('title',
                  'description',
                  'isDone')
