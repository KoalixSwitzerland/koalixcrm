from rest_framework import serializers

from koalixcrm.crm.reporting.resource import Resource
from koalixcrm.crm.reporting.resource_type import ResourceType
from koalixcrm.crm.reporting.resource_manager import ResourceManager
from koalixcrm.crm.rest.resource_manager_rest import OptionResourceManagerJSONSerializer
from koalixcrm.crm.rest.resource_type_rest import OptionResourceTypeJSONSerializer


class OptionResourceJSONSerializer(serializers.HyperlinkedModelSerializer):
    resourceType = OptionResourceTypeJSONSerializer(required=False, read_only=True)
    resourceManager = OptionResourceManagerJSONSerializer(read_only=True)

    class Meta:
        model = Resource
        fields = ('resource_type',
                  'resource_manager')


class ResourceJSONSerializer(serializers.HyperlinkedModelSerializer):
    resourceType = OptionResourceTypeJSONSerializer()
    resourceManager = OptionResourceManagerJSONSerializer()

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
        resource_manager = validated_data.pop('resourceManager')
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
        resource_manager = validated_data.pop('resourceManager')
        if resource_manager:
            if resource_manager.get('id', resource.resource_manager):
                resource.resource_manager = ResourceManager.objects.get(id=resource.get('id', None))
            else:
                resource.resource_manager = resource.resource_manager_id
        else:
            resource.resource_manager = None
