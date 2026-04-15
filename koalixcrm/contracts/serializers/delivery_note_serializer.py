# -*- coding: utf-8 -*-
from rest_framework import serializers
from koalixcrm.contracts.models.delivery_note import DeliveryNote


class DeliveryNoteJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryNote
        fields = '__all__'
