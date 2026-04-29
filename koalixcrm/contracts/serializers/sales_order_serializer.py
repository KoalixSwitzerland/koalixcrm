# -*- coding: utf-8 -*-
from rest_framework import serializers

from koalixcrm.contracts.models.sales_order import SalesOrder


class SalesOrderJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesOrder
        fields = '__all__'
