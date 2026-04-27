from rest_framework import serializers

from koalixcrm.reporting.models.task_status import TaskStatus


class OptionTaskStatusJSONSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    title = serializers.CharField(required=False)
    description = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    is_done = serializers.BooleanField(read_only=True)

    class Meta:
        model = TaskStatus
        fields = ('id',
                  'title',
                  'description',
                  'is_done')


class TaskStatusJSONSerializer(serializers.ModelSerializer):
    is_done = serializers.BooleanField()

    class Meta:
        model = TaskStatus
        fields = ('id',
                  'title',
                  'description',
                  'is_done')
