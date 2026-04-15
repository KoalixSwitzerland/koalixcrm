# -*- coding: utf-8 -*-
from rest_framework import serializers
from koalixcrm.contracts.models.payment_reminder import PaymentReminder


class PaymentReminderJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentReminder
        fields = '__all__'
