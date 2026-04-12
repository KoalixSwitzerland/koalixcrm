from rest_framework import serializers
from koalixcrm.reporting.models.resource_type import ResourceType


class OptionResourceTypeJSONSerializer(serializers.HyperlinkedModelSerializer):
    title = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)

    class Meta:
        model = ResourceType
        fields = ('title',
                  'description')


class ResourceTypeJSONSerializer(serializers.HyperlinkedModelSerializer):
    title = serializers.CharField()
    description = serializers.CharField()

    class Meta:
        model = ResourceType
        fields = ('title',
                  'description')
