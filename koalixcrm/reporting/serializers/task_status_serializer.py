from rest_framework import serializers
from koalixcrm.reporting.models.task_status import TaskStatus


class OptionTaskStatusJSONSerializer(serializers.HyperlinkedModelSerializer):
    is_done = serializers.BooleanField(read_only=True)

    class Meta:
        model = TaskStatus
        fields = ('title',
                  'description',
                  'is_done')


class TaskStatusJSONSerializer(serializers.HyperlinkedModelSerializer):
    is_done = serializers.BooleanField()

    class Meta:
        model = TaskStatus
        fields = ('title',
                  'description',
                  'is_done')
