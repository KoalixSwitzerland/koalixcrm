# -*- coding: utf-8 -*-
from rest_framework import serializers
from koalixcrm.contracts.models.purchase_confirmation import PurchaseConfirmation


class PurchaseConfirmationJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseConfirmation
        fields = '__all__'
