# -*- coding: utf-8 -*-
"""
Contacts API entry point.

Exposes Contacts REST viewsets for URL routing.
"""
from koalixcrm.contacts.views.customer_view_set import CustomerViewSet
from koalixcrm.contacts.views.customer_group_view_set import CustomerGroupViewSet
from koalixcrm.contacts.views.customer_billing_cycle_view_set import CustomerBillingCycleViewSet
from koalixcrm.contacts.views.contact_postal_address_view_set import ContactPostalAddressViewSet
from koalixcrm.contacts.views.contact_email_address_view_set import ContactEmailAddressViewSet
from koalixcrm.contacts.views.contact_phone_address_view_set import ContactPhoneAddressViewSet
from koalixcrm.contacts.views.supplier_view_set import SupplierViewSet
from koalixcrm.contacts.views.person_view_set import PersonViewSet
from koalixcrm.contacts.views.contact_view_set import ContactViewSet
from koalixcrm.contacts.views.party_view_sets import (
    PartyViewSet,
    OrganizationViewSet,
    PartyContactViewSet,
    PartyIdentificationViewSet,
    PartyRoleViewSet,
    OrganizationMembershipViewSet,
    OrganizationRelationshipViewSet,
    AddressViewSet,
    AddressAssignmentViewSet,
    PhoneNumberViewSet,
    PhoneAssignmentViewSet,
    PartyEmailViewSet,
    EmailAssignmentViewSet,
    PartyGroupViewSet,
    PartyGroupMembershipViewSet,
)

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
    # Party data model (issue #394).
    'PartyViewSet',
    'OrganizationViewSet',
    'PartyContactViewSet',
    'PartyIdentificationViewSet',
    'PartyRoleViewSet',
    'OrganizationMembershipViewSet',
    'OrganizationRelationshipViewSet',
    'AddressViewSet',
    'AddressAssignmentViewSet',
    'PhoneNumberViewSet',
    'PhoneAssignmentViewSet',
    'PartyEmailViewSet',
    'EmailAssignmentViewSet',
    'PartyGroupViewSet',
    'PartyGroupMembershipViewSet',
]
