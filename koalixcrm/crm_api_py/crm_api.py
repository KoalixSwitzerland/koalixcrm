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
from koalixcrm.crm.views.supplier_view_set import SupplierViewSet
from koalixcrm.crm.views.person_view_set import PersonViewSet
from koalixcrm.crm.views.contact_view_set import ContactViewSet

__all__ = [
    'CustomerViewSet',
    'CustomerGroupViewSet',
    'CustomerBillingCycleViewSet',
    'ContactPostalAddressViewSet',
    'ContactEmailAddressViewSet',
    'ContactPhoneAddressViewSet',
    'SupplierViewSet',
    'PersonViewSet',
    'ContactViewSet',
]
