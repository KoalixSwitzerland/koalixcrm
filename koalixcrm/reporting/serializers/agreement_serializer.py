# -*- coding: utf-8 -*-
from rest_framework import serializers

from koalixcrm.core.models.unit import Unit
from koalixcrm.core.serializers.unit_serializer import OptionUnitJSONSerializer
from koalixcrm.reporting.models.agreement import Agreement
from koalixcrm.reporting.models.agreement_status import AgreementStatus
from koalixcrm.reporting.models.agreement_type import AgreementType
from koalixcrm.reporting.models.resource import Resource
from koalixcrm.reporting.models.resource_price import ResourcePrice
from koalixcrm.reporting.models.task import Task
from koalixcrm.reporting.serializers.agreement_status_serializer import (
    OptionAgreementStatusJSONSerializer,
)
from koalixcrm.reporting.serializers.agreement_type_serializer import (
    OptionAgreementTypeJSONSerializer,
)
from koalixcrm.reporting.serializers.resource_price_serializer import (
    OptionResourcePriceJSONSerializer,
)
from koalixcrm.reporting.serializers.resource_serializer import (
    OptionResourceJSONSerializer,
)
from koalixcrm.reporting.serializers.task_serializer import OptionTaskJSONSerializer


class AgreementJSONSerializer(serializers.ModelSerializer):
    task = OptionTaskJSONSerializer(allow_null=False)
    resource = OptionResourceJSONSerializer(allow_null=False)
    unit = OptionUnitJSONSerializer(allow_null=False)
    type = OptionAgreementTypeJSONSerializer(allow_null=False)
    status = OptionAgreementStatusJSONSerializer(allow_null=False)
    costs = OptionResourcePriceJSONSerializer(allow_null=False)

    class Meta:
        model = Agreement
        fields = ('id',
                  'amount',
                  'date_from',
                  'date_until',
                  'task',
                  'resource',
                  'unit',
                  'costs',
                  'type',
                  'status')

    def create(self, validated_data):
        agreement = Agreement()
        agreement.amount = validated_data['amount']
        agreement.date_from = validated_data['date_from']
        agreement.date_until = validated_data['date_until']
        # Deserialize task
        task = validated_data.pop('task')
        if task:
            if task.get('id', None):
                agreement.task = Task.objects.get(id=task.get('id', None))
            else:
                agreement.task = None
        # Deserialize resource
        resource = validated_data.pop('resource')
        if resource:
            if resource.get('id', None):
                agreement.resource = Resource.objects.get(id=resource.get('id', None))
            else:
                agreement.resource = None
        # Deserialize unit
        unit = validated_data.pop('unit')
        if unit:
            if unit.get('id', None):
                agreement.unit = Unit.objects.get(id=unit.get('id', None))
            else:
                agreement.unit = None
        # Deserialize costs
        costs = validated_data.pop('costs')
        if costs:
            if costs.get('id', None):
                agreement.costs = ResourcePrice.objects.get(id=costs.get('id', None))
            else:
                agreement.costs = None
        # Deserialize type
        type = validated_data.pop('type')
        if type:
            if type.get('id', None):
                agreement.type = AgreementType.objects.get(id=type.get('id', None))
            else:
                agreement.type = None
        # Deserialize status
        status = validated_data.pop('status')
        if status:
            if type.get('id', None):
                agreement.status = AgreementStatus.objects.get(id=status.get('id', None))
            else:
                agreement.status = None

        agreement.save()
        return agreement

    def update(self, agreement, validated_data):
        agreement.amount = validated_data['amount']
        agreement.date_from = validated_data['date_from']
        agreement.date_until = validated_data['date_until']
        task = validated_data.pop('task')
        if task:
            if task.get('id', agreement.task):
                agreement.task = Task.objects.get(id=task.get('id', None))
            else:
                agreement.task = agreement.task_id
        else:
            agreement.task = None
        # Deserialize resource
        resource = validated_data.pop('resource')
        if resource:
            if resource.get('id', agreement.resource):
                agreement.resource = Resource.objects.get(id=resource.get('id', None))
            else:
                agreement.resource = agreement.resource_id
        else:
            agreement.resource = None
        # Deserialize unit
        unit = validated_data.pop('unit')
        if task:
            if unit.get('id', agreement.unit):
                agreement.unit = Unit.objects.get(id=unit.get('id', None))
            else:
                agreement.unit = agreement.unit_id
        else:
            agreement.unit = None
        # Deserialize costs
        costs = validated_data.pop('costs')
        if costs:
            if costs.get('id', agreement.costs):
                agreement.costs = ResourcePrice.objects.get(id=costs.get('id', None))
            else:
                agreement.costs = agreement.costs_id
        else:
            agreement.costs = None
        # Deserialize type
        type = validated_data.pop('type')
        if type:
            if type.get('id', None):
                agreement.type = AgreementType.objects.get(id=type.get('id', None))
            else:
                agreement.type = agreement.type_id
        else:
            agreement.type = None
        # Deserialize status
        status = validated_data.pop('status')
        if status:
            if status.get('id', agreement.status):
                agreement.status = AgreementStatus.objects.get(id=status.get('id', None))
            else:
                agreement.status = agreement.status_id
        else:
            agreement.status = None

        agreement.save()

        return agreement
