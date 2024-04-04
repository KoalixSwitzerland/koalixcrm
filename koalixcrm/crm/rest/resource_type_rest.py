from rest_framework import serializers
from koalixcrm.crm.reporting.resource_type import ResourceType


class OptionResourceTypeJSONSerializer(serializers.HyperlinkedModelSerializer):
    title = serializers.CharField(source='title', read_only=True)
    description = serializers.CharField(source='description', read_only=True)

    class Meta:
        model = ResourceType
        fields = ('title',
                  'description')


class ResourceTypeJSONSerializer(serializers.HyperlinkedModelSerializer):
    title = serializers.CharField(source='title')
    description = serializers.CharField(source='description')

    class Meta:
        model = ResourceType
        fields = ('title',
                  'description')
