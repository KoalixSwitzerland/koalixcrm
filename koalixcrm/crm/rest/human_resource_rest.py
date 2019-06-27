from rest_framework import serializers

from koalixcrm.djangoUserExtension.user_extension.user_extension import UserExtension
from koalixcrm.crm.reporting.human_resource import HumanResource
from koalixcrm.crm.reporting.resource_type import ResourceType
from koalixcrm.crm.reporting.resource_manager import ResourceManager
from koalixcrm.djangoUserExtension.rest.user_extension_rest import OptionUserExtensionJSONSerializer
from koalixcrm.crm.rest.resource_manager_rest import OptionResourceManagerJSONSerializer
from koalixcrm.crm.rest.resource_type_rest import OptionResourceTypeJSONSerializer


class OptionHumanResourceJSONSerializer(serializers.HyperlinkedModelSerializer):
    resourceType = OptionResourceTypeJSONSerializer(source='resource_type',
                                                    required=False,
                                                    read_only=True)
    resourceManager = OptionResourceManagerJSONSerializer(source='resource_manager',
                                                          read_only=True)
    user = OptionResourceManagerJSONSerializer(source='user',
                                               read_only=True)

    class Meta:
        model = HumanResource
        fields = ('user',
                  'resource_manager',
                  'resource_type')


class HumanResourceJSONSerializer(serializers.HyperlinkedModelSerializer):
    resourceType = OptionResourceTypeJSONSerializer(source='resource_type')
    resourceManager = OptionResourceManagerJSONSerializer(source='resource_manager')
    user = OptionResourceManagerJSONSerializer(source='user')

    class Meta:
        model = HumanResource
        fields = ('user',
                  'resource_type',
                  'resource_manager')

    def create(self, validated_data):
        resource = HumanResource()
        # Deserialize resource_type
        resource_type = validated_data.pop('resourceType')
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
        # Deserialize resource_manager
        user = validated_data.pop('user')
        if user:
            if user.get('id', None):
                resource.user = UserExtension.objects.get(id=user.get('id', None))
            else:
                resource.user = None

    def update(self, resource, validated_data):
        # Deserialize resource_type
        resource_type = validated_data.pop('resourceType')
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
        # Deserialize user
        user = validated_data.pop('user')
        if user:
            if user.get('id', resource.resource_manager):
                resource.user = UserExtension.objects.get(id=user.get('id', None))
            else:
                resource.user = resource.user_id
        else:
            resource.user = None
