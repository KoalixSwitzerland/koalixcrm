from __future__ import annotations

from rest_framework import serializers

from koalixcrm.reporting.models.estimation_status import EstimationStatus


class OptionEstimationStatusJSONSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    title = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    is_obsolete = serializers.BooleanField(read_only=True)

    class Meta:
        model = EstimationStatus
        fields = ('id',
                  'title',
                  'description',
                  'is_obsolete')


class EstimationStatusJSONSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    description = serializers.CharField()
    is_obsolete = serializers.BooleanField()

    class Meta:
        model = EstimationStatus
        fields = ('id',
                  'title',
                  'description',
                  'is_obsolete')
