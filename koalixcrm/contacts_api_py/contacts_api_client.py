# -*- coding: utf-8 -*-
"""KoalixCRM Contacts API Client (post-v2.0.0).

The legacy Customer / Supplier / Person / Contact / CustomerGroup /
Contact{Postal,Phone,Email}Address endpoints and their client methods
are gone as of v2.0.0 (issue #395). Everything goes through the Party
data model DTOs below.
"""
from typing import Dict, List, Any, Optional

from koalixcrm.shared.api_client import BaseAPIClient
from koalixcrm.contacts_api_py.dto.customer_billing_cycle import CustomerBillingCycle
from koalixcrm.contacts_api_py.dto.party_dtos import (
    Party as PartyDto,
    Organization as OrganizationDto,
    PartyContact as PartyContactDto,
    PartyIdentification as PartyIdentificationDto,
    PartyRole as PartyRoleDto,
    OrganizationMembership as OrganizationMembershipDto,
    OrganizationRelationship as OrganizationRelationshipDto,
    Address as AddressDto,
    AddressAssignment as AddressAssignmentDto,
    PhoneNumber as PhoneNumberDto,
    PhoneAssignment as PhoneAssignmentDto,
    PartyEmail as PartyEmailDto,
    EmailAssignment as EmailAssignmentDto,
    PartyGroup as PartyGroupDto,
    PartyGroupMembership as PartyGroupMembershipDto,
)


class KoalixCRMContactsAPIClient(BaseAPIClient):
    api_path_env_var = 'KOALIXCRM_CONTACTS_API_PATH'
    api_path_default = ''

    def __init__(self, api_url=None, username=None, password=None):
        super().__init__(api_url=api_url, username=username, password=password)

    # ------------------------------------------------------------------
    # CustomerBillingCycle (endpoint: /customer_billing_cycles)
    # ------------------------------------------------------------------

    def get_customer_billing_cycle(self, object_id: int) -> Optional[CustomerBillingCycle]:
        return self._get_object(CustomerBillingCycle, "/customer_billing_cycles", object_id)

    def get_customer_billing_cycle_list(self) -> List[CustomerBillingCycle]:
        return self._get_object_list(CustomerBillingCycle, "/customer_billing_cycles/")

    def create_customer_billing_cycle(self, data: Dict[str, Any]) -> Optional[CustomerBillingCycle]:
        response_data = self._make_request("/customer_billing_cycles/", method="POST", data=data)
        if response_data:
            obj = CustomerBillingCycle(response_data, self)
            self._cache.set(CustomerBillingCycle, obj.id, obj)
            return obj
        return None

    def update_customer_billing_cycle(self, object_id: int, data: Dict[str, Any]) -> Optional[CustomerBillingCycle]:
        return self._put_full_update(CustomerBillingCycle, "/customer_billing_cycles", object_id, data)

    # ------------------------------------------------------------------
    # Party data model (issue #394). One get/list/create/update quartet
    # per /api/... resource registered in projectsettings/urls.py.
    # ------------------------------------------------------------------

    # --- Party ---
    def get_party(self, object_id: int) -> Optional[PartyDto]:
        return self._get_object(PartyDto, "/parties", object_id)

    def get_party_list(self) -> List[PartyDto]:
        return self._get_object_list(PartyDto, "/parties/")

    def create_party(self, data: Dict[str, Any]) -> Optional[PartyDto]:
        response_data = self._make_request("/parties/", method="POST", data=data)
        if response_data:
            obj = PartyDto(response_data, self)
            self._cache.set(PartyDto, obj.id, obj)
            return obj
        return None

    def update_party(self, object_id: int, data: Dict[str, Any]) -> Optional[PartyDto]:
        return self._put_full_update(PartyDto, "/parties", object_id, data)

    # --- Organization ---
    def get_organization(self, object_id: int) -> Optional[OrganizationDto]:
        return self._get_object(OrganizationDto, "/organizations", object_id)

    def get_organization_list(self) -> List[OrganizationDto]:
        return self._get_object_list(OrganizationDto, "/organizations/")

    def create_organization(self, data: Dict[str, Any]) -> Optional[OrganizationDto]:
        response_data = self._make_request("/organizations/", method="POST", data=data)
        if response_data:
            obj = OrganizationDto(response_data, self)
            self._cache.set(OrganizationDto, obj.id, obj)
            return obj
        return None

    def update_organization(self, object_id: int, data: Dict[str, Any]) -> Optional[OrganizationDto]:
        return self._put_full_update(OrganizationDto, "/organizations", object_id, data)

    # --- PartyContact (natural person) ---
    def get_party_contact(self, object_id: int) -> Optional[PartyContactDto]:
        return self._get_object(PartyContactDto, "/party_contacts", object_id)

    def get_party_contact_list(self) -> List[PartyContactDto]:
        return self._get_object_list(PartyContactDto, "/party_contacts/")

    def create_party_contact(self, data: Dict[str, Any]) -> Optional[PartyContactDto]:
        response_data = self._make_request("/party_contacts/", method="POST", data=data)
        if response_data:
            obj = PartyContactDto(response_data, self)
            self._cache.set(PartyContactDto, obj.id, obj)
            return obj
        return None

    def update_party_contact(self, object_id: int, data: Dict[str, Any]) -> Optional[PartyContactDto]:
        return self._put_full_update(PartyContactDto, "/party_contacts", object_id, data)

    # --- PartyIdentification ---
    def get_party_identification(self, object_id: int) -> Optional[PartyIdentificationDto]:
        return self._get_object(PartyIdentificationDto, "/party_identifications", object_id)

    def get_party_identification_list(self) -> List[PartyIdentificationDto]:
        return self._get_object_list(PartyIdentificationDto, "/party_identifications/")

    def create_party_identification(self, data: Dict[str, Any]) -> Optional[PartyIdentificationDto]:
        response_data = self._make_request("/party_identifications/", method="POST", data=data)
        if response_data:
            obj = PartyIdentificationDto(response_data, self)
            self._cache.set(PartyIdentificationDto, obj.id, obj)
            return obj
        return None

    def update_party_identification(self, object_id: int, data: Dict[str, Any]) -> Optional[PartyIdentificationDto]:
        return self._put_full_update(PartyIdentificationDto, "/party_identifications", object_id, data)

    # --- PartyRole ---
    def get_party_role(self, object_id: int) -> Optional[PartyRoleDto]:
        return self._get_object(PartyRoleDto, "/party_roles", object_id)

    def get_party_role_list(self) -> List[PartyRoleDto]:
        return self._get_object_list(PartyRoleDto, "/party_roles/")

    def create_party_role(self, data: Dict[str, Any]) -> Optional[PartyRoleDto]:
        response_data = self._make_request("/party_roles/", method="POST", data=data)
        if response_data:
            obj = PartyRoleDto(response_data, self)
            self._cache.set(PartyRoleDto, obj.id, obj)
            return obj
        return None

    def update_party_role(self, object_id: int, data: Dict[str, Any]) -> Optional[PartyRoleDto]:
        return self._put_full_update(PartyRoleDto, "/party_roles", object_id, data)

    # --- OrganizationMembership ---
    def get_organization_membership(self, object_id: int) -> Optional[OrganizationMembershipDto]:
        return self._get_object(OrganizationMembershipDto, "/organization_memberships", object_id)

    def get_organization_membership_list(self) -> List[OrganizationMembershipDto]:
        return self._get_object_list(OrganizationMembershipDto, "/organization_memberships/")

    def create_organization_membership(self, data: Dict[str, Any]) -> Optional[OrganizationMembershipDto]:
        response_data = self._make_request("/organization_memberships/", method="POST", data=data)
        if response_data:
            obj = OrganizationMembershipDto(response_data, self)
            self._cache.set(OrganizationMembershipDto, obj.id, obj)
            return obj
        return None

    def update_organization_membership(self, object_id: int, data: Dict[str, Any]) -> Optional[OrganizationMembershipDto]:
        return self._put_full_update(OrganizationMembershipDto, "/organization_memberships", object_id, data)

    # --- OrganizationRelationship ---
    def get_organization_relationship(self, object_id: int) -> Optional[OrganizationRelationshipDto]:
        return self._get_object(OrganizationRelationshipDto, "/organization_relationships", object_id)

    def get_organization_relationship_list(self) -> List[OrganizationRelationshipDto]:
        return self._get_object_list(OrganizationRelationshipDto, "/organization_relationships/")

    def create_organization_relationship(self, data: Dict[str, Any]) -> Optional[OrganizationRelationshipDto]:
        response_data = self._make_request("/organization_relationships/", method="POST", data=data)
        if response_data:
            obj = OrganizationRelationshipDto(response_data, self)
            self._cache.set(OrganizationRelationshipDto, obj.id, obj)
            return obj
        return None

    def update_organization_relationship(self, object_id: int, data: Dict[str, Any]) -> Optional[OrganizationRelationshipDto]:
        return self._put_full_update(OrganizationRelationshipDto, "/organization_relationships", object_id, data)

    # --- Address (new standalone) ---
    def get_address(self, object_id: int) -> Optional[AddressDto]:
        return self._get_object(AddressDto, "/addresses", object_id)

    def get_address_list(self) -> List[AddressDto]:
        return self._get_object_list(AddressDto, "/addresses/")

    def create_address(self, data: Dict[str, Any]) -> Optional[AddressDto]:
        response_data = self._make_request("/addresses/", method="POST", data=data)
        if response_data:
            obj = AddressDto(response_data, self)
            self._cache.set(AddressDto, obj.id, obj)
            return obj
        return None

    def update_address(self, object_id: int, data: Dict[str, Any]) -> Optional[AddressDto]:
        return self._put_full_update(AddressDto, "/addresses", object_id, data)

    # --- AddressAssignment ---
    def get_address_assignment(self, object_id: int) -> Optional[AddressAssignmentDto]:
        return self._get_object(AddressAssignmentDto, "/address_assignments", object_id)

    def get_address_assignment_list(self) -> List[AddressAssignmentDto]:
        return self._get_object_list(AddressAssignmentDto, "/address_assignments/")

    def create_address_assignment(self, data: Dict[str, Any]) -> Optional[AddressAssignmentDto]:
        response_data = self._make_request("/address_assignments/", method="POST", data=data)
        if response_data:
            obj = AddressAssignmentDto(response_data, self)
            self._cache.set(AddressAssignmentDto, obj.id, obj)
            return obj
        return None

    def update_address_assignment(self, object_id: int, data: Dict[str, Any]) -> Optional[AddressAssignmentDto]:
        return self._put_full_update(AddressAssignmentDto, "/address_assignments", object_id, data)

    # --- PhoneNumber ---
    def get_phone_number(self, object_id: int) -> Optional[PhoneNumberDto]:
        return self._get_object(PhoneNumberDto, "/phone_numbers", object_id)

    def get_phone_number_list(self) -> List[PhoneNumberDto]:
        return self._get_object_list(PhoneNumberDto, "/phone_numbers/")

    def create_phone_number(self, data: Dict[str, Any]) -> Optional[PhoneNumberDto]:
        response_data = self._make_request("/phone_numbers/", method="POST", data=data)
        if response_data:
            obj = PhoneNumberDto(response_data, self)
            self._cache.set(PhoneNumberDto, obj.id, obj)
            return obj
        return None

    def update_phone_number(self, object_id: int, data: Dict[str, Any]) -> Optional[PhoneNumberDto]:
        return self._put_full_update(PhoneNumberDto, "/phone_numbers", object_id, data)

    # --- PhoneAssignment ---
    def get_phone_assignment(self, object_id: int) -> Optional[PhoneAssignmentDto]:
        return self._get_object(PhoneAssignmentDto, "/phone_assignments", object_id)

    def get_phone_assignment_list(self) -> List[PhoneAssignmentDto]:
        return self._get_object_list(PhoneAssignmentDto, "/phone_assignments/")

    def create_phone_assignment(self, data: Dict[str, Any]) -> Optional[PhoneAssignmentDto]:
        response_data = self._make_request("/phone_assignments/", method="POST", data=data)
        if response_data:
            obj = PhoneAssignmentDto(response_data, self)
            self._cache.set(PhoneAssignmentDto, obj.id, obj)
            return obj
        return None

    def update_phone_assignment(self, object_id: int, data: Dict[str, Any]) -> Optional[PhoneAssignmentDto]:
        return self._put_full_update(PhoneAssignmentDto, "/phone_assignments", object_id, data)

    # --- PartyEmail ---
    def get_party_email(self, object_id: int) -> Optional[PartyEmailDto]:
        return self._get_object(PartyEmailDto, "/party_emails", object_id)

    def get_party_email_list(self) -> List[PartyEmailDto]:
        return self._get_object_list(PartyEmailDto, "/party_emails/")

    def create_party_email(self, data: Dict[str, Any]) -> Optional[PartyEmailDto]:
        response_data = self._make_request("/party_emails/", method="POST", data=data)
        if response_data:
            obj = PartyEmailDto(response_data, self)
            self._cache.set(PartyEmailDto, obj.id, obj)
            return obj
        return None

    def update_party_email(self, object_id: int, data: Dict[str, Any]) -> Optional[PartyEmailDto]:
        return self._put_full_update(PartyEmailDto, "/party_emails", object_id, data)

    # --- EmailAssignment ---
    def get_email_assignment(self, object_id: int) -> Optional[EmailAssignmentDto]:
        return self._get_object(EmailAssignmentDto, "/email_assignments", object_id)

    def get_email_assignment_list(self) -> List[EmailAssignmentDto]:
        return self._get_object_list(EmailAssignmentDto, "/email_assignments/")

    def create_email_assignment(self, data: Dict[str, Any]) -> Optional[EmailAssignmentDto]:
        response_data = self._make_request("/email_assignments/", method="POST", data=data)
        if response_data:
            obj = EmailAssignmentDto(response_data, self)
            self._cache.set(EmailAssignmentDto, obj.id, obj)
            return obj
        return None

    def update_email_assignment(self, object_id: int, data: Dict[str, Any]) -> Optional[EmailAssignmentDto]:
        return self._put_full_update(EmailAssignmentDto, "/email_assignments", object_id, data)

    # --- PartyGroup ---
    def get_party_group(self, object_id: int) -> Optional[PartyGroupDto]:
        return self._get_object(PartyGroupDto, "/party_groups", object_id)

    def get_party_group_list(self) -> List[PartyGroupDto]:
        return self._get_object_list(PartyGroupDto, "/party_groups/")

    def create_party_group(self, data: Dict[str, Any]) -> Optional[PartyGroupDto]:
        response_data = self._make_request("/party_groups/", method="POST", data=data)
        if response_data:
            obj = PartyGroupDto(response_data, self)
            self._cache.set(PartyGroupDto, obj.id, obj)
            return obj
        return None

    def update_party_group(self, object_id: int, data: Dict[str, Any]) -> Optional[PartyGroupDto]:
        return self._put_full_update(PartyGroupDto, "/party_groups", object_id, data)

    # --- PartyGroupMembership ---
    def get_party_group_membership(self, object_id: int) -> Optional[PartyGroupMembershipDto]:
        return self._get_object(PartyGroupMembershipDto, "/party_group_memberships", object_id)

    def get_party_group_membership_list(self) -> List[PartyGroupMembershipDto]:
        return self._get_object_list(PartyGroupMembershipDto, "/party_group_memberships/")

    def create_party_group_membership(self, data: Dict[str, Any]) -> Optional[PartyGroupMembershipDto]:
        response_data = self._make_request("/party_group_memberships/", method="POST", data=data)
        if response_data:
            obj = PartyGroupMembershipDto(response_data, self)
            self._cache.set(PartyGroupMembershipDto, obj.id, obj)
            return obj
        return None

    def update_party_group_membership(self, object_id: int, data: Dict[str, Any]) -> Optional[PartyGroupMembershipDto]:
        return self._put_full_update(PartyGroupMembershipDto, "/party_group_memberships", object_id, data)
