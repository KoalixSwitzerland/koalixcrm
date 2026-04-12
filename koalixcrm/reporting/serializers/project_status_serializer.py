from rest_framework import serializers
from koalixcrm.reporting.models.project_status import ProjectStatus


class OptionProjectStatusJSONSerializer(serializers.HyperlinkedModelSerializer):
    is_done = serializers.BooleanField(read_only=True)

    class Meta:
        model = ProjectStatus
        fields = ('title',
                  'description',
                  'is_done')


class ProjectStatusJSONSerializer(serializers.HyperlinkedModelSerializer):
    is_done = serializers.BooleanField()

    class Meta:
        model = ProjectStatus
        fields = ('title',
                  'description',
                  'is_done')
