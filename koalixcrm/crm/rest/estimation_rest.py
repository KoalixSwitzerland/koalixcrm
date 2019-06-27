# -*- coding: utf-8 -*-
from rest_framework import serializers
from koalixcrm.crm.reporting.estimation import Estimation
from koalixcrm.crm.reporting.estimation_status import EstimationStatus
from koalixcrm.crm.reporting.resource import Resource
from koalixcrm.crm.reporting.task import Task
from koalixcrm.crm.rest.task_rest import OptionTaskJSONSerializer
from koalixcrm.crm.rest.estimation_status_rest import OptionEstimationStatusJSONSerializer
from koalixcrm.crm.rest.resource_rest import OptionResourceJSONSerializer


class EstimationJSONSerializer(serializers.HyperlinkedModelSerializer):
    task = OptionTaskJSONSerializer(source='task', allow_null=False)
    resource = OptionResourceJSONSerializer(source='resource', allow_null=False)
    status = OptionEstimationStatusJSONSerializer(source='status', allow_null=False)
    dateFrom = serializers.DateField(source='date_from')
    dateUntil = serializers.DateField(source='date_until')
    amount = serializers.DecimalField(source='amount')

    class Meta:
        model = Estimation
        fields = ('task',
                  'resource',
                  'amount',
                  'date_from',
                  'date_until',
                  'status',
                  'reporting_period')

    def create(self, validated_data):
        estimation = Estimation()
        estimation.amount = validated_data['amount']
        estimation.date_from = validated_data['dateFrom']
        estimation.date_until = validated_data['dateUntil']
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
            if type.get('id', None):
                estimation.status = EstimationStatus.objects.get(id=status.get('id', None))
            else:
                estimation.status = None

        estimation.save()
        return estimation

    def update(self, estimation, validated_data):
        estimation.amount = validated_data['amount']
        estimation.date_from = validated_data['dateFrom']
        estimation.date_until = validated_data['dateUntil']
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



