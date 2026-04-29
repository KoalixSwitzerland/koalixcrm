from __future__ import annotations

from typing import Any

from rest_framework import serializers

from koalixcrm.djangoUserExtension.models.user_extension import UserExtension
from koalixcrm.djangoUserExtension.serializers.user_extension_rest import (
    OptionUserExtensionJSONSerializer,
)
from koalixcrm.reporting.models.resource_manager import ResourceManager


class OptionResourceManagerJSONSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    user = OptionUserExtensionJSONSerializer(read_only=True)

    class Meta:
        model = ResourceManager
        fields = ('id',
                  'user',)


class ResourceManagerJSONSerializer(serializers.ModelSerializer):
    user = OptionUserExtensionJSONSerializer()

    class Meta:
        model = ResourceManager
        fields = ('user',)

    def create(self, validated_data: dict[str, Any]) -> None:
        resource_manager = ResourceManager()
        if 'workspace' in validated_data:
            resource_manager.workspace = validated_data.pop('workspace')
        # Deserialize user
        user = validated_data.pop('user')
        if user:
            if user.get('id', None):
                resource_manager.user = UserExtension.objects.get(id=user.get('id', None))
            else:
                resource_manager.user = None

    def update(self, resource_manager: ResourceManager, validated_data: dict[str, Any]) -> None:
        # Deserialize user
        user = validated_data.pop('user')
        if user:
            if user.get('id', resource_manager.resource_manager):
                resource_manager.user = UserExtension.objects.get(id=user.get('id', None))
            else:
                resource_manager.user = resource_manager.user_id
        else:
            resource_manager.user = None
