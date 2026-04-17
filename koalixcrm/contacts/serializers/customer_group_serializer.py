from rest_framework import serializers

from koalixcrm.contacts.models.customer_group import CustomerGroup


class OptionCustomerGroupJSONSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(read_only=True)

    class Meta:
        model = CustomerGroup
        fields = ('id',
                  'name')


class CustomerGroupJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerGroup
        fields = ('id',
                  'name')
