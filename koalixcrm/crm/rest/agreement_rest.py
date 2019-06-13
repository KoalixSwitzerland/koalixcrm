# -*- coding: utf-8 -*-
from rest_framework import serializers
from koalixcrm.crm.reporting.agreement import Agreement
from koalixcrm.crm.reporting.agreement_type import AgreementType
from koalixcrm.crm.reporting.agreement_status import AgreementStatus
from koalixcrm.crm.reporting.resource_price import ResourcePrice
from koalixcrm.crm.reporting.resource import Resource
from koalixcrm.crm.reporting.task import Task
from koalixcrm.crm.product.unit import Unit
from koalixcrm.crm.rest.task_rest import OptionTaskJSONSerializer
from koalixcrm.crm.rest.unit_rest import OptionUnitJSONSerializer
from koalixcrm.crm.rest.resource_price_rest import OptionResourcePriceJSONSerializer
from koalixcrm.crm.rest.agreement_type_rest import OptionAgreementTypeJSONSerializer
from koalixcrm.crm.rest.agreement_status_rest import OptionAgreementStatusJSONSerializer
from koalixcrm.crm.rest.resource_rest import OptionResourceJSONSerializer


class AgreementJSONSerializer(serializers.HyperlinkedModelSerializer):
    task = OptionTaskJSONSerializer(source='task', allow_null=False)
    resource = OptionResourceJSONSerializer(source='resource', allow_null=False)
    unit = OptionUnitJSONSerializer(source='unit', allow_null=False)
    type = OptionAgreementTypeJSONSerializer(source='type', allow_null=False)
    status = OptionAgreementStatusJSONSerializer(source='status', allow_null=False)
    costs = OptionResourcePriceJSONSerializer(source='costs', allow_null=False)

    class Meta:
        model = Agreement
        fields = ('amount',
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
        agreement.date_from = validated_data['dateFrom']
        agreement.date_until = validated_data['dateUntil']
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
        agreement.date_from = validated_data['dateFrom']
        agreement.date_until = validated_data['dateUntil']
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
            if type.get('id', agreement.type):
                agreement.type = Task.objects.get(id=type.get('id', None))
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



