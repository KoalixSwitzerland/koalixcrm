from rest_framework import serializers

from koalixcrm.reporting.models.resource import Resource
from koalixcrm.reporting.models.resource_manager import ResourceManager
from koalixcrm.reporting.models.resource_type import ResourceType
from koalixcrm.reporting.serializers.resource_manager_serializer import (
    OptionResourceManagerJSONSerializer,
)
from koalixcrm.reporting.serializers.resource_type_serializer import (
    OptionResourceTypeJSONSerializer,
)


class OptionResourceJSONSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    resource_type = OptionResourceTypeJSONSerializer(required=False, read_only=True)
    resource_manager = OptionResourceManagerJSONSerializer(read_only=True)

    class Meta:
        model = Resource
        fields = ('id',
                  'resource_type',
                  'resource_manager')


class ResourceJSONSerializer(serializers.ModelSerializer):
    resource_type = OptionResourceTypeJSONSerializer()
    resource_manager = OptionResourceManagerJSONSerializer()

    class Meta:
        model = Resource
        fields = ('resource_type',
                  'resource_manager')

    def create(self, validated_data):
        resource = Resource()
        # Deserialize resource_type
        resource_type = validated_data.pop('resource_type')
        if resource_type:
            if resource_type.get('id', None):
                resource.resource_type = ResourceType.objects.get(id=resource_type.get('id', None))
            else:
                resource.resource_type = None
        # Deserialize resource_manager
        resource_manager = validated_data.pop('resource_manager')
        if resource_manager:
            if resource_manager.get('id', None):
                resource.resource_manager = ResourceManager.objects.get(id=resource_manager.get('id', None))
            else:
                resource.resource_manager = None

    def update(self, resource, validated_data):
        # Deserialize resource_type
        resource_type = validated_data.pop('resource_type')
        if resource_type:
            if resource_type.get('id', resource.resource_type):
                resource.resource_type = ResourceType.objects.get(id=resource_type.get('id', None))
            else:
                resource.resource_type = resource.resource_type_id
        else:
            resource.resource_type = None
        # Deserialize resource_manager
        resource_manager = validated_data.pop('resource_manager')
        if resource_manager:
            if resource_manager.get('id', resource.resource_manager):
                resource.resource_manager = ResourceManager.objects.get(id=resource.get('id', None))
            else:
                resource.resource_manager = resource.resource_manager_id
        else:
            resource.resource_manager = None
