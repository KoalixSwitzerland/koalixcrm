from rest_framework import serializers
from koalixcrm.crm.reporting.project_status import ProjectStatus


class OptionProjectStatusJSONSerializer(serializers.HyperlinkedModelSerializer):
    title = serializers.CharField(source='title', read_only=True)
    description = serializers.CharField(source='description', read_only=True)
    isDone = serializers.BooleanField(source='is_done', read_only=True)

    class Meta:
        model = ProjectStatus
        fields = ('title',
                  'description',
                  'is_done')


class ProjectStatusJSONSerializer(serializers.HyperlinkedModelSerializer):
    title = serializers.CharField(source='title')
    description = serializers.CharField(source='description')
    isDone = serializers.BooleanField(source='is_done')

    class Meta:
        model = ProjectStatus
        fields = ('title',
                  'description',
                  'is_done')
