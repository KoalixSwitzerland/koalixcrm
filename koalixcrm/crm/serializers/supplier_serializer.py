# -*- coding: utf-8 -*-
from rest_framework import serializers

from koalixcrm.crm.contact.supplier import Supplier


class SupplierJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'
