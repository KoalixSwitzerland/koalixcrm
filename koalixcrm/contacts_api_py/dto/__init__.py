# -*- coding: utf-8 -*-
"""CRM DTO classes."""

from koalixcrm.contacts_api_py.dto.contact import Contact
from koalixcrm.contacts_api_py.dto.customer import Customer
from koalixcrm.contacts_api_py.dto.supplier import Supplier
from koalixcrm.contacts_api_py.dto.customer_group import CustomerGroup
from koalixcrm.contacts_api_py.dto.customer_billing_cycle import CustomerBillingCycle
from koalixcrm.contacts_api_py.dto.person import Person

# Party data model DTOs (issue #394).
from koalixcrm.contacts_api_py.dto.party_dtos import (
    Party,
    Organization,
    PartyContact,
    PartyIdentification,
    PartyRole,
    OrganizationMembership,
    OrganizationRelationship,
    Address,
    AddressAssignment,
    PhoneNumber,
    PhoneAssignment,
    PartyEmail,
    EmailAssignment,
    PartyGroup,
    PartyGroupMembership,
)
