# -*- coding: utf-8 -*-
"""Contacts API entry point.

Exposes Contacts REST viewsets for URL routing. Post-v2.0.0 the legacy
Customer / Supplier / Person / Contact / CustomerGroup viewsets are gone;
everything goes through the Party data model.
"""
from koalixcrm.contacts.views.customer_billing_cycle_view_set import (
    CustomerBillingCycleViewSet,
)
from koalixcrm.contacts.views.party_view_sets import (
    AddressAssignmentViewSet,
    AddressViewSet,
    EmailAssignmentViewSet,
    OrganizationMembershipViewSet,
    OrganizationRelationshipViewSet,
    OrganizationViewSet,
    PartyContactViewSet,
    PartyEmailViewSet,
    PartyGroupMembershipViewSet,
    PartyGroupViewSet,
    PartyIdentificationViewSet,
    PartyRoleViewSet,
    PartyViewSet,
    PhoneAssignmentViewSet,
    PhoneNumberViewSet,
)

__all__ = [
    'CustomerBillingCycleViewSet',
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
