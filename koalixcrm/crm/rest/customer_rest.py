from rest_framework import serializers

from koalixcrm.crm.contact.customer import Customer
from koalixcrm.crm.rest.contact_rest import ContactJSONSerializer
from koalixcrm.crm.rest.customer_billing_cycle_rest import OptionCustomerBillingCycleJSONSerializer
from koalixcrm.crm.rest.customer_group_rest import OptionCustomerGroupJSONSerializer


class CustomerJSONSerializer(ContactJSONSerializer):
    defaultCustomerBillingCycle = OptionCustomerBillingCycleJSONSerializer(source='default_customer_billing_cycle')
    isMemberOf = OptionCustomerGroupJSONSerializer(source='is_member_of', many=True)
    isLead = serializers.BooleanField(source='is_lead')

    class Meta:
        model = Customer
        fields = ContactJSONSerializer.Meta.fields + (
            'defaultCustomerBillingCycle',
            'isMemberOf',
            'isLead', )
