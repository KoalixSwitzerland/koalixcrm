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
    daysToPaymentDate = serializers.IntegerField(source='time_to_payment_date', allow_null=False)
    paymentReminderDaysToPayment = serializers.IntegerField(source='payment_reminder_time_to_payment', allow_null=True)

    class Meta:
        model = CustomerBillingCycle
        fields = ('id',
                  'name',
                  'daysToPaymentDate',
                  'paymentReminderDaysToPayment')
