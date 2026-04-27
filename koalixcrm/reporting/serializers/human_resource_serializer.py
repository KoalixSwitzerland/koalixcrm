from rest_framework import serializers

from koalixcrm.djangoUserExtension.models.user_extension import UserExtension
from koalixcrm.djangoUserExtension.serializers.user_extension_rest import (
    OptionUserExtensionJSONSerializer,
)
from koalixcrm.reporting.models.human_resource import HumanResource
from koalixcrm.reporting.models.resource_manager import ResourceManager
from koalixcrm.reporting.models.resource_type import ResourceType
from koalixcrm.reporting.serializers.resource_manager_serializer import (
    OptionResourceManagerJSONSerializer,
)
from koalixcrm.reporting.serializers.resource_type_serializer import (
    OptionResourceTypeJSONSerializer,
)


class OptionHumanResourceJSONSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    resource_type = OptionResourceTypeJSONSerializer(required=False,
                                                     read_only=True)
    resource_manager = OptionResourceManagerJSONSerializer(read_only=True)
    user = OptionUserExtensionJSONSerializer(read_only=True)

    class Meta:
        model = HumanResource
        fields = ('id',
                  'user',
                  'resource_manager',
                  'resource_type')


class HumanResourceJSONSerializer(serializers.ModelSerializer):
    resource_type = OptionResourceTypeJSONSerializer()
    resource_manager = OptionResourceManagerJSONSerializer()
    user = OptionUserExtensionJSONSerializer()

    class Meta:
        model = HumanResource
        fields = ('id',
                  'user',
                  'resource_type',
                  'resource_manager')

    def create(self, validated_data):
        resource = HumanResource()
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
        # Deserialize resource_manager
        user = validated_data.pop('user')
        if user:
            if user.get('id', None):
                resource.user = UserExtension.objects.get(id=user.get('id', None))
            else:
                resource.user = None
        resource.save()
        return resource

    def update(self, resource, validated_data):
        # Deserialize resource_type
        resource_type = validated_data.pop('resource_type')
        if resource_type:
            if resource_type.get('id', None):
                resource.resource_type = ResourceType.objects.get(id=resource_type.get('id', None))
            else:
                resource.resource_type = resource.resource_type_id
        else:
            resource.resource_type = None
        # Deserialize resource_manager
        resource_manager = validated_data.pop('resource_manager')
        if resource_manager:
            if resource_manager.get('id', None):
                resource.resource_manager = ResourceManager.objects.get(id=resource_manager.get('id', None))
            else:
                resource.resource_manager = resource.resource_manager_id
        else:
            resource.resource_manager = None
        # Deserialize user
        user = validated_data.pop('user')
        if user:
            if user.get('id', None):
                resource.user = UserExtension.objects.get(id=user.get('id', None))
            else:
                resource.user = resource.user_id
        else:
            resource.user = None
        resource.save()
        return resource
