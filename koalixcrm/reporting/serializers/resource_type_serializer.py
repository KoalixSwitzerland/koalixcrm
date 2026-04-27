from rest_framework import serializers

from koalixcrm.reporting.models.resource_type import ResourceType


class OptionResourceTypeJSONSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    title = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)

    class Meta:
        model = ResourceType
        fields = ('id',
                  'title',
                  'description')


class ResourceTypeJSONSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    description = serializers.CharField()

    class Meta:
        model = ResourceType
        fields = ('title',
                  'description')
