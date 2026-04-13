# -*- coding: utf-8 -*-
from rest_framework import serializers
from koalixcrm.contracts.models.contract import Contract


class ContractJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ('id',
                  'staff',
                  'description',
                  'default_customer',
                  'default_currency',
                  'default_template_set',
                  'last_modified_by')
