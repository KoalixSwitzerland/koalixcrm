# -*- coding: utf-8 -*-
from rest_framework import serializers
from koalixcrm.contracts.models.credit_note import CreditNote


class CreditNoteJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditNote
        fields = '__all__'
