# -*- coding: utf-8 -*-
"""
CRM API entry point.

Exposes CRM (contacts) REST viewsets for URL routing.
"""
from koalixcrm.crm.views.customer_view_set import CustomerViewSet
from koalixcrm.crm.views.customer_group_view_set import CustomerGroupViewSet
from koalixcrm.crm.views.customer_billing_cycle_view_set import CustomerBillingCycleViewSet
from koalixcrm.crm.views.contact_postal_address_view_set import ContactPostalAddressViewSet
from koalixcrm.crm.views.contact_email_address_view_set import ContactEmailAddressViewSet
from koalixcrm.crm.views.contact_phone_address_view_set import ContactPhoneAddressViewSet

__all__ = [
    'CustomerViewSet',
    'CustomerGroupViewSet',
    'CustomerBillingCycleViewSet',
    'ContactPostalAddressViewSet',
    'ContactEmailAddressViewSet',
    'ContactPhoneAddressViewSet',
]
