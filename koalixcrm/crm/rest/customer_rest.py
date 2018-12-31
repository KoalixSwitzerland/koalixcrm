from rest_framework import serializers

from koalixcrm.crm.contact.customer import Customer
from koalixcrm.crm.rest.contact_rest import ContactJSONSerializer


class CustomerJSONSerializer(ContactJSONSerializer):
    isLead = serializers.BooleanField(source='is_lead')

    class Meta:
        model = Customer
        fields = ContactJSONSerializer.Meta.fields + ('isLead', )
