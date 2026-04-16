from rest_framework import serializers

from koalixcrm.contacts.models.customer_billing_cycle import CustomerBillingCycle


class OptionCustomerBillingCycleJSONSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(read_only=True)

    class Meta:
        model = CustomerBillingCycle
        fields = ('id',
                  'name')


class CustomerBillingCycleJSONSerializer(serializers.ModelSerializer):
    time_to_payment_date = serializers.IntegerField(allow_null=False)
    payment_reminder_time_to_payment = serializers.IntegerField(allow_null=True)

    class Meta:
        model = CustomerBillingCycle
        fields = ('id',
                  'name',
                  'time_to_payment_date',
                  'payment_reminder_time_to_payment')
