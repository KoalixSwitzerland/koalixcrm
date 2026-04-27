from rest_framework import serializers

from koalixcrm.reporting.models.project_status import ProjectStatus


class OptionProjectStatusJSONSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    title = serializers.CharField(required=False)
    description = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    is_done = serializers.BooleanField(read_only=True)

    class Meta:
        model = ProjectStatus
        fields = ('id',
                  'title',
                  'description',
                  'is_done')


class ProjectStatusJSONSerializer(serializers.ModelSerializer):
    is_done = serializers.BooleanField()

    class Meta:
        model = ProjectStatus
        fields = ('id',
                  'title',
                  'description',
                  'is_done')
