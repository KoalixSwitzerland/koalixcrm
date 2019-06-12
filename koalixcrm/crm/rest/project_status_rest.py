from rest_framework import serializers
from koalixcrm.crm.reporting.project_status import ProjectStatus


class OptionProjectStatusJSONSerializer(serializers.HyperlinkedModelSerializer):
    isDone = serializers.BooleanField(source='is_done', read_only=True)

    class Meta:
        model = ProjectStatus
        fields = ('title',
                  'description',
                  'isDone')


class ProjectStatusJSONSerializer(serializers.HyperlinkedModelSerializer):
    isDone = serializers.BooleanField(source='is_done')

    class Meta:
        model = ProjectStatus
        fields = ('title',
                  'description',
                  'isDone')
