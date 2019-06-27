from rest_framework import serializers

from koalixcrm.djangoUserExtension.user_extension.user_extension import UserExtension
from koalixcrm.crm.reporting.resource_manager import ResourceManager
from koalixcrm.djangoUserExtension.rest.user_extension_rest import OptionUserExtensionJSONSerializer


class OptionResourceManagerJSONSerializer(serializers.HyperlinkedModelSerializer):
    user = OptionUserExtensionJSONSerializer(source='user',
                                             read_only=True)

    class Meta:
        model = ResourceManager
        fields = ('user',)


class ResourceManagerJSONSerializer(serializers.HyperlinkedModelSerializer):
    user = OptionUserExtensionJSONSerializer(source='user')

    class Meta:
        model = ResourceManager
        fields = ('user',)

    def create(self, validated_data):
        resource_manager = ResourceManager()
        # Deserialize user
        user = validated_data.pop('user')
        if user:
            if user.get('id', None):
                resource_manager.user = UserExtension.objects.get(id=user.get('id', None))
            else:
                resource_manager.user = None

    def update(self, resource_manager, validated_data):
        # Deserialize user
        user = validated_data.pop('user')
        if user:
            if user.get('id', resource_manager.resource_manager):
                resource_manager.user = UserExtension.objects.get(id=user.get('id', None))
            else:
                resource_manager.user = resource_manager.user_id
        else:
            resource_manager.user = None
