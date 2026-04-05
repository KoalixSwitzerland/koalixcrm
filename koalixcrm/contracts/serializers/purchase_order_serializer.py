# -*- coding: utf-8 -*-
from rest_framework import serializers
from koalixcrm.contracts.models.purchase_order import PurchaseOrder


class PurchaseOrderJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'
