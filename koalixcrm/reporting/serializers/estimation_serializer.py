# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Any

from rest_framework import serializers

from koalixcrm.reporting.models.estimation import Estimation
from koalixcrm.reporting.models.estimation_status import EstimationStatus
from koalixcrm.reporting.models.resource import Resource
from koalixcrm.reporting.models.task import Task
from koalixcrm.reporting.serializers.estimation_status_serializer import (
    OptionEstimationStatusJSONSerializer,
)
from koalixcrm.reporting.serializers.resource_serializer import (
    OptionResourceJSONSerializer,
)
from koalixcrm.reporting.serializers.task_serializer import OptionTaskJSONSerializer


class EstimationJSONSerializer(serializers.ModelSerializer):
    task = OptionTaskJSONSerializer(allow_null=False)
    resource = OptionResourceJSONSerializer(allow_null=False)
    status = OptionEstimationStatusJSONSerializer(allow_null=False)
    date_from = serializers.DateField()
    date_until = serializers.DateField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Estimation
        fields = ('id',
                  'task',
                  'resource',
                  'amount',
                  'date_from',
                  'date_until',
                  'status',
                  'reporting_period')

    def create(self, validated_data: dict[str, Any]) -> Estimation:
        estimation = Estimation()
        if 'workspace' in validated_data:
            estimation.workspace = validated_data.pop('workspace')
        estimation.amount = validated_data['amount']
        estimation.date_from = validated_data['date_from']
        estimation.date_until = validated_data['date_until']
        # Deserialize task
        task = validated_data.pop('task')
        if task:
            if task.get('id', None):
                estimation.task = Task.objects.get(id=task.get('id', None))
            else:
                estimation.task = None
        # Deserialize resource
        resource = validated_data.pop('resource')
        if resource:
            if resource.get('id', None):
                estimation.resource = Resource.objects.get(id=resource.get('id', None))
            else:
                estimation.resource = None
        # Deserialize status
        status = validated_data.pop('status')
        if status:
            if status.get('id', None):
                estimation.status = EstimationStatus.objects.get(id=status.get('id', None))
            else:
                estimation.status = None
        # Set reporting_period (PK field)
        reporting_period = validated_data.get('reporting_period')
        if reporting_period:
            estimation.reporting_period = reporting_period

        estimation.save()
        return estimation

    def update(self, estimation: Estimation, validated_data: dict[str, Any]) -> Estimation:
        estimation.amount = validated_data['amount']
        estimation.date_from = validated_data['date_from']
        estimation.date_until = validated_data['date_until']
        task = validated_data.pop('task')
        if task:
            if task.get('id', estimation.task):
                estimation.task = Task.objects.get(id=task.get('id', None))
            else:
                estimation.task = estimation.task_id
        else:
            estimation.task = None
        # Deserialize resource
        resource = validated_data.pop('resource')
        if resource:
            if resource.get('id', estimation.resource):
                estimation.resource = Resource.objects.get(id=resource.get('id', None))
            else:
                estimation.resource = estimation.resource_id
        else:
            estimation.resource = None
        # Deserialize status
        status = validated_data.pop('status')
        if status:
            if status.get('id', estimation.status):
                estimation.status = EstimationStatus.objects.get(id=status.get('id', None))
            else:
                estimation.status = estimation.status_id
        else:
            estimation.status = None

        estimation.save()

        return estimation
