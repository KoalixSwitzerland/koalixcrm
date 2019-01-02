from rest_framework import serializers

from koalixcrm.crm.contact.customer_group import CustomerGroup


class OptionCustomerGroupJSONSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(read_only=True)

    class Meta:
        model = CustomerGroup
        fields = ('id',
                  'name')


class CustomerGroupJSONSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomerGroup
        fields = ('id',
                  'name')
