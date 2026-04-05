# -*- coding: utf-8 -*-
from rest_framework import serializers
from koalixcrm.contracts.models.contract import Contract


class ContractJSONSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contract
        fields = ('id',
                  'description')
