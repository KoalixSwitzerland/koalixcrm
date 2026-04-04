# -*- coding: utf-8 -*-
from koalixcrm.crm.serializers.contact_serializer import (
    ContactJSONSerializer,
    ContactPhoneAddressJSONSerializer,
    ContactEmailAddressJSONSerializer,
    ContactPostalAddressJSONSerializer,
    PhoneAddressJSONSerializer,
    EmailAddressJSONSerializer,
    PostalAddressJSONSerializer,
)
from koalixcrm.crm.serializers.customer_serializer import CustomerJSONSerializer
from koalixcrm.crm.serializers.customer_group_serializer import (
    OptionCustomerGroupJSONSerializer,
    CustomerGroupJSONSerializer,
)
from koalixcrm.crm.serializers.customer_billing_cycle_serializer import (
    OptionCustomerBillingCycleJSONSerializer,
    CustomerBillingCycleJSONSerializer,
)

__all__ = [
    'ContactJSONSerializer',
    'ContactPhoneAddressJSONSerializer',
    'ContactEmailAddressJSONSerializer',
    'ContactPostalAddressJSONSerializer',
    'PhoneAddressJSONSerializer',
    'EmailAddressJSONSerializer',
    'PostalAddressJSONSerializer',
    'CustomerJSONSerializer',
    'OptionCustomerGroupJSONSerializer',
    'CustomerGroupJSONSerializer',
    'OptionCustomerBillingCycleJSONSerializer',
    'CustomerBillingCycleJSONSerializer',
]
