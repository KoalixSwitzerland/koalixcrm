# -*- coding: utf-8 -*-
from rest_framework import serializers

from koalixcrm.products.models.customer_group_transform import CustomerGroupTransform


class CustomerGroupTransformJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerGroupTransform
        fields = '__all__'
