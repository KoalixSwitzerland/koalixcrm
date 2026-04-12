from rest_framework import serializers

from koalixcrm.crm.contact.customer_billing_cycle import CustomerBillingCycle


class OptionCustomerBillingCycleJSONSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(read_only=True)

    class Meta:
        model = CustomerBillingCycle
        fields = ('id',
                  'name')


class CustomerBillingCycleJSONSerializer(serializers.HyperlinkedModelSerializer):
    time_to_payment_date = serializers.IntegerField(allow_null=False)
    payment_reminder_time_to_payment = serializers.IntegerField(allow_null=True)

    class Meta:
        model = CustomerBillingCycle
        fields = ('id',
                  'name',
                  'time_to_payment_date',
                  'payment_reminder_time_to_payment')
