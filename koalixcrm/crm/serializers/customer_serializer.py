from django.contrib.auth.models import User
from rest_framework import serializers

from koalixcrm.crm.contact.customer import Customer
from koalixcrm.crm.contact.customer_billing_cycle import CustomerBillingCycle
from koalixcrm.crm.contact.customer_group import CustomerGroup
from koalixcrm.crm.serializers.contact_serializer import ContactJSONSerializer
from koalixcrm.crm.serializers.customer_billing_cycle_serializer import OptionCustomerBillingCycleJSONSerializer
from koalixcrm.crm.serializers.customer_group_serializer import OptionCustomerGroupJSONSerializer


class CustomerJSONSerializer(ContactJSONSerializer):
    default_customer_billing_cycle = OptionCustomerBillingCycleJSONSerializer()
    is_member_of = OptionCustomerGroupJSONSerializer(many=True)
    is_lead = serializers.BooleanField()

    class Meta:
        model = Customer
        fields = ContactJSONSerializer.Meta.fields + (
            'id',
            'default_customer_billing_cycle',
            'is_member_of',
            'is_lead', )

    def create(self, validated_data):
        customer = Customer()
        customer.name = validated_data['name']
        customer.is_lead = validated_data['is_lead']

        # Deserialize from default billing cycle
        billing_cycle = validated_data.pop('default_customer_billing_cycle')
        if billing_cycle:
            if billing_cycle.get('id', None):
                customer.default_customer_billing_cycle = CustomerBillingCycle.objects.get(id=billing_cycle.get('id', None))
            else:
                customer.default_customer_billing_cycle = None

        # Deserialize from staff
        request = self.context.get('request')
        koalixcrm_user = request.META.get('HTTP_KOALIXCRM_USER')
        user = User.objects.get(username=koalixcrm_user)
        customer.last_modified_by = user

        customer.save()

        # Deserialize from customer group
        # Customer object has to be saved before to be able to add some many to many items. After adding a new many to
        # many item, the save action for the customer object is not needed since it's executed anyway.
        customer_groups = validated_data.pop('is_member_of')
        if customer_groups:
            for customerGroup in customer_groups:
                if customerGroup.get('id', None):
                    customer.is_member_of.add(CustomerGroup.objects.get(id=customerGroup.get('id', None)))

        return customer

    def update(self, customer, validated_data):
        customer.name = validated_data.get('name', customer.name)
        customer.is_lead = validated_data.get('is_lead', customer.is_lead)

        # Deserialize from staff
        request = self.context.get('request')
        koalixcrm_user = request.META.get('HTTP_KOALIXCRM_USER')
        user = User.objects.get(username=koalixcrm_user)
        customer.last_modified_by = user

        # Deserialize from customer group
        # Clear all from existing customer and add the deserialized items again.
        customer_groups = validated_data.pop('is_member_of')
        customer.is_member_of.clear()
        if customer_groups:
            for customerGroup in customer_groups:
                if customerGroup.get('id', None):
                    customer.is_member_of.add(CustomerGroup.objects.get(id=customerGroup.get('id', None)))

        customer.save()

        return customer
