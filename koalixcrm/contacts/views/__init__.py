# -*- coding: utf-8 -*-
from .contact_view_set import ContactViewSet
from .contact_email_address_view_set import ContactEmailAddressViewSet
from .contact_phone_address_view_set import ContactPhoneAddressViewSet
from .contact_postal_address_view_set import ContactPostalAddressViewSet
from .customer_view_set import CustomerViewSet
from .customer_group_view_set import CustomerGroupViewSet
from .customer_billing_cycle_view_set import CustomerBillingCycleViewSet
from .supplier_view_set import SupplierViewSet
from .person_view_set import PersonViewSet
from .party_view_sets import (
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
    'ContactViewSet',
    'ContactEmailAddressViewSet',
    'ContactPhoneAddressViewSet',
    'ContactPostalAddressViewSet',
    'CustomerViewSet',
    'CustomerGroupViewSet',
    'CustomerBillingCycleViewSet',
    'SupplierViewSet',
    'PersonViewSet',
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
