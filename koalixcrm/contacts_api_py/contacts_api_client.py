# -*- coding: utf-8 -*-
"""KoalixCRM Contacts API Client (post-v2.0.0).

The legacy Customer / Supplier / Person / Contact / CustomerGroup /
Contact{Postal,Phone,Email}Address endpoints and their client methods
are gone as of v2.0.0 (issue #395). Everything goes through the Party
data model DTOs below.
"""

from __future__ import annotations

from typing import Any

from koalixcrm.contacts_api_py.dto.customer_billing_cycle import CustomerBillingCycle
from koalixcrm.contacts_api_py.dto.party_dtos import (
    Address as AddressDto,
)
from koalixcrm.contacts_api_py.dto.party_dtos import (
    AddressAssignment as AddressAssignmentDto,
)
from koalixcrm.contacts_api_py.dto.party_dtos import (
    EmailAssignment as EmailAssignmentDto,
)
from koalixcrm.contacts_api_py.dto.party_dtos import (
    Organization as OrganizationDto,
)
from koalixcrm.contacts_api_py.dto.party_dtos import (
    OrganizationMembership as OrganizationMembershipDto,
)
from koalixcrm.contacts_api_py.dto.party_dtos import (
    OrganizationRelationship as OrganizationRelationshipDto,
)
from koalixcrm.contacts_api_py.dto.party_dtos import (
    Party as PartyDto,
)
from koalixcrm.contacts_api_py.dto.party_dtos import (
    PartyContact as PartyContactDto,
)
from koalixcrm.contacts_api_py.dto.party_dtos import (
    PartyEmail as PartyEmailDto,
)
from koalixcrm.contacts_api_py.dto.party_dtos import (
    PartyGroup as PartyGroupDto,
)
from koalixcrm.contacts_api_py.dto.party_dtos import (
    PartyGroupMembership as PartyGroupMembershipDto,
)
from koalixcrm.contacts_api_py.dto.party_dtos import (
    PartyIdentification as PartyIdentificationDto,
)
from koalixcrm.contacts_api_py.dto.party_dtos import (
    PartyRole as PartyRoleDto,
)
from koalixcrm.contacts_api_py.dto.party_dtos import (
    PhoneAssignment as PhoneAssignmentDto,
)
from koalixcrm.contacts_api_py.dto.party_dtos import (
    PhoneNumber as PhoneNumberDto,
)
from koalixcrm.shared.api_client import BaseAPIClient


class KoalixCRMContactsAPIClient(BaseAPIClient):
    api_path_env_var = "KOALIXCRM_CONTACTS_API_PATH"
    api_path_default = "/koalixcrm_contacts/api/v1/"
    uses_workspace_id = True

    def __init__(
        self,
        api_url: str | None = None,
        username: str | None = None,
        password: str | None = None,
        workspace_id: int | None = None,
    ) -> None:
        super().__init__(api_url=api_url, username=username, password=password, workspace_id=workspace_id)

    # ------------------------------------------------------------------
    # CustomerBillingCycle (endpoint: /customer_billing_cycles)
    # ------------------------------------------------------------------

    def get_customer_billing_cycle(self, object_id: int) -> CustomerBillingCycle | None:
        return self._get_object(CustomerBillingCycle, "/customer-billing-cycles", object_id)

    def get_customer_billing_cycle_list(self) -> list[CustomerBillingCycle]:
        return self._get_object_list(CustomerBillingCycle, "/customer-billing-cycles/")

    def create_customer_billing_cycle(self, data: dict[str, Any]) -> CustomerBillingCycle | None:
        response_data = self._make_request("/customer-billing-cycles/", method="POST", data=data)
        if response_data:
            obj = CustomerBillingCycle(response_data, self)
            self._cache.set(CustomerBillingCycle, obj.id, obj)
            return obj
        return None

    def update_customer_billing_cycle(self, object_id: int, data: dict[str, Any]) -> CustomerBillingCycle | None:
        return self._put_full_update(CustomerBillingCycle, "/customer-billing-cycles", object_id, data)

    # ------------------------------------------------------------------
    # Party data model (issue #394). One get/list/create/update quartet
    # per /api/... resource registered in projectsettings/urls.py.
    # ------------------------------------------------------------------

    # --- Party ---
    def get_party(self, object_id: int) -> PartyDto | None:
        return self._get_object(PartyDto, "/parties", object_id)

    def get_party_list(self) -> list[PartyDto]:
        return self._get_object_list(PartyDto, "/parties/")

    def create_party(self, data: dict[str, Any]) -> PartyDto | None:
        response_data = self._make_request("/parties/", method="POST", data=data)
        if response_data:
            obj = PartyDto(response_data, self)
            self._cache.set(PartyDto, obj.id, obj)
            return obj
        return None

    def update_party(self, object_id: int, data: dict[str, Any]) -> PartyDto | None:
        return self._put_full_update(PartyDto, "/parties", object_id, data)

    # --- Organization ---
    def get_organization(self, object_id: int) -> OrganizationDto | None:
        return self._get_object(OrganizationDto, "/organizations", object_id)

    def get_organization_list(self) -> list[OrganizationDto]:
        return self._get_object_list(OrganizationDto, "/organizations/")

    def create_organization(self, data: dict[str, Any]) -> OrganizationDto | None:
        response_data = self._make_request("/organizations/", method="POST", data=data)
        if response_data:
            obj = OrganizationDto(response_data, self)
            self._cache.set(OrganizationDto, obj.id, obj)
            return obj
        return None

    def update_organization(self, object_id: int, data: dict[str, Any]) -> OrganizationDto | None:
        return self._put_full_update(OrganizationDto, "/organizations", object_id, data)

    # --- PartyContact (natural person) ---
    def get_party_contact(self, object_id: int) -> PartyContactDto | None:
        return self._get_object(PartyContactDto, "/party-contacts", object_id)

    def get_party_contact_list(self) -> list[PartyContactDto]:
        return self._get_object_list(PartyContactDto, "/party-contacts/")

    def create_party_contact(self, data: dict[str, Any]) -> PartyContactDto | None:
        response_data = self._make_request("/party-contacts/", method="POST", data=data)
        if response_data:
            obj = PartyContactDto(response_data, self)
            self._cache.set(PartyContactDto, obj.id, obj)
            return obj
        return None

    def update_party_contact(self, object_id: int, data: dict[str, Any]) -> PartyContactDto | None:
        return self._put_full_update(PartyContactDto, "/party-contacts", object_id, data)

    # --- PartyIdentification ---
    def get_party_identification(self, object_id: int) -> PartyIdentificationDto | None:
        return self._get_object(PartyIdentificationDto, "/party-identifications", object_id)

    def get_party_identification_list(self) -> list[PartyIdentificationDto]:
        return self._get_object_list(PartyIdentificationDto, "/party-identifications/")

    def create_party_identification(self, data: dict[str, Any]) -> PartyIdentificationDto | None:
        response_data = self._make_request("/party-identifications/", method="POST", data=data)
        if response_data:
            obj = PartyIdentificationDto(response_data, self)
            self._cache.set(PartyIdentificationDto, obj.id, obj)
            return obj
        return None

    def update_party_identification(self, object_id: int, data: dict[str, Any]) -> PartyIdentificationDto | None:
        return self._put_full_update(PartyIdentificationDto, "/party-identifications", object_id, data)

    # --- PartyRole ---
    def get_party_role(self, object_id: int) -> PartyRoleDto | None:
        return self._get_object(PartyRoleDto, "/party-roles", object_id)

    def get_party_role_list(self) -> list[PartyRoleDto]:
        return self._get_object_list(PartyRoleDto, "/party-roles/")

    def create_party_role(self, data: dict[str, Any]) -> PartyRoleDto | None:
        response_data = self._make_request("/party-roles/", method="POST", data=data)
        if response_data:
            obj = PartyRoleDto(response_data, self)
            self._cache.set(PartyRoleDto, obj.id, obj)
            return obj
        return None

    def update_party_role(self, object_id: int, data: dict[str, Any]) -> PartyRoleDto | None:
        return self._put_full_update(PartyRoleDto, "/party-roles", object_id, data)

    # --- OrganizationMembership ---
    def get_organization_membership(self, object_id: int) -> OrganizationMembershipDto | None:
        return self._get_object(OrganizationMembershipDto, "/organization-memberships", object_id)

    def get_organization_membership_list(self) -> list[OrganizationMembershipDto]:
        return self._get_object_list(OrganizationMembershipDto, "/organization-memberships/")

    def create_organization_membership(self, data: dict[str, Any]) -> OrganizationMembershipDto | None:
        response_data = self._make_request("/organization-memberships/", method="POST", data=data)
        if response_data:
            obj = OrganizationMembershipDto(response_data, self)
            self._cache.set(OrganizationMembershipDto, obj.id, obj)
            return obj
        return None

    def update_organization_membership(
        self, object_id: int, data: dict[str, Any]
    ) -> OrganizationMembershipDto | None:
        return self._put_full_update(OrganizationMembershipDto, "/organization-memberships", object_id, data)

    # --- OrganizationRelationship ---
    def get_organization_relationship(self, object_id: int) -> OrganizationRelationshipDto | None:
        return self._get_object(OrganizationRelationshipDto, "/organization-relationships", object_id)

    def get_organization_relationship_list(self) -> list[OrganizationRelationshipDto]:
        return self._get_object_list(OrganizationRelationshipDto, "/organization-relationships/")

    def create_organization_relationship(self, data: dict[str, Any]) -> OrganizationRelationshipDto | None:
        response_data = self._make_request("/organization-relationships/", method="POST", data=data)
        if response_data:
            obj = OrganizationRelationshipDto(response_data, self)
            self._cache.set(OrganizationRelationshipDto, obj.id, obj)
            return obj
        return None

    def update_organization_relationship(
        self, object_id: int, data: dict[str, Any]
    ) -> OrganizationRelationshipDto | None:
        return self._put_full_update(OrganizationRelationshipDto, "/organization-relationships", object_id, data)

    # --- Address (new standalone) ---
    def get_address(self, object_id: int) -> AddressDto | None:
        return self._get_object(AddressDto, "/addresses", object_id)

    def get_address_list(self) -> list[AddressDto]:
        return self._get_object_list(AddressDto, "/addresses/")

    def create_address(self, data: dict[str, Any]) -> AddressDto | None:
        response_data = self._make_request("/addresses/", method="POST", data=data)
        if response_data:
            obj = AddressDto(response_data, self)
            self._cache.set(AddressDto, obj.id, obj)
            return obj
        return None

    def update_address(self, object_id: int, data: dict[str, Any]) -> AddressDto | None:
        return self._put_full_update(AddressDto, "/addresses", object_id, data)

    # --- AddressAssignment ---
    def get_address_assignment(self, object_id: int) -> AddressAssignmentDto | None:
        return self._get_object(AddressAssignmentDto, "/address-assignments", object_id)

    def get_address_assignment_list(self) -> list[AddressAssignmentDto]:
        return self._get_object_list(AddressAssignmentDto, "/address-assignments/")

    def create_address_assignment(self, data: dict[str, Any]) -> AddressAssignmentDto | None:
        response_data = self._make_request("/address-assignments/", method="POST", data=data)
        if response_data:
            obj = AddressAssignmentDto(response_data, self)
            self._cache.set(AddressAssignmentDto, obj.id, obj)
            return obj
        return None

    def update_address_assignment(self, object_id: int, data: dict[str, Any]) -> AddressAssignmentDto | None:
        return self._put_full_update(AddressAssignmentDto, "/address-assignments", object_id, data)

    # --- PhoneNumber ---
    def get_phone_number(self, object_id: int) -> PhoneNumberDto | None:
        return self._get_object(PhoneNumberDto, "/phone-numbers", object_id)

    def get_phone_number_list(self) -> list[PhoneNumberDto]:
        return self._get_object_list(PhoneNumberDto, "/phone-numbers/")

    def create_phone_number(self, data: dict[str, Any]) -> PhoneNumberDto | None:
        response_data = self._make_request("/phone-numbers/", method="POST", data=data)
        if response_data:
            obj = PhoneNumberDto(response_data, self)
            self._cache.set(PhoneNumberDto, obj.id, obj)
            return obj
        return None

    def update_phone_number(self, object_id: int, data: dict[str, Any]) -> PhoneNumberDto | None:
        return self._put_full_update(PhoneNumberDto, "/phone-numbers", object_id, data)

    # --- PhoneAssignment ---
    def get_phone_assignment(self, object_id: int) -> PhoneAssignmentDto | None:
        return self._get_object(PhoneAssignmentDto, "/phone-assignments", object_id)

    def get_phone_assignment_list(self) -> list[PhoneAssignmentDto]:
        return self._get_object_list(PhoneAssignmentDto, "/phone-assignments/")

    def create_phone_assignment(self, data: dict[str, Any]) -> PhoneAssignmentDto | None:
        response_data = self._make_request("/phone-assignments/", method="POST", data=data)
        if response_data:
            obj = PhoneAssignmentDto(response_data, self)
            self._cache.set(PhoneAssignmentDto, obj.id, obj)
            return obj
        return None

    def update_phone_assignment(self, object_id: int, data: dict[str, Any]) -> PhoneAssignmentDto | None:
        return self._put_full_update(PhoneAssignmentDto, "/phone-assignments", object_id, data)

    # --- PartyEmail ---
    def get_party_email(self, object_id: int) -> PartyEmailDto | None:
        return self._get_object(PartyEmailDto, "/party-emails", object_id)

    def get_party_email_list(self) -> list[PartyEmailDto]:
        return self._get_object_list(PartyEmailDto, "/party-emails/")

    def create_party_email(self, data: dict[str, Any]) -> PartyEmailDto | None:
        response_data = self._make_request("/party-emails/", method="POST", data=data)
        if response_data:
            obj = PartyEmailDto(response_data, self)
            self._cache.set(PartyEmailDto, obj.id, obj)
            return obj
        return None

    def update_party_email(self, object_id: int, data: dict[str, Any]) -> PartyEmailDto | None:
        return self._put_full_update(PartyEmailDto, "/party-emails", object_id, data)

    # --- EmailAssignment ---
    def get_email_assignment(self, object_id: int) -> EmailAssignmentDto | None:
        return self._get_object(EmailAssignmentDto, "/email-assignments", object_id)

    def get_email_assignment_list(self) -> list[EmailAssignmentDto]:
        return self._get_object_list(EmailAssignmentDto, "/email-assignments/")

    def create_email_assignment(self, data: dict[str, Any]) -> EmailAssignmentDto | None:
        response_data = self._make_request("/email-assignments/", method="POST", data=data)
        if response_data:
            obj = EmailAssignmentDto(response_data, self)
            self._cache.set(EmailAssignmentDto, obj.id, obj)
            return obj
        return None

    def update_email_assignment(self, object_id: int, data: dict[str, Any]) -> EmailAssignmentDto | None:
        return self._put_full_update(EmailAssignmentDto, "/email-assignments", object_id, data)

    # --- PartyGroup ---
    def get_party_group(self, object_id: int) -> PartyGroupDto | None:
        return self._get_object(PartyGroupDto, "/party-groups", object_id)

    def get_party_group_list(self) -> list[PartyGroupDto]:
        return self._get_object_list(PartyGroupDto, "/party-groups/")

    def create_party_group(self, data: dict[str, Any]) -> PartyGroupDto | None:
        response_data = self._make_request("/party-groups/", method="POST", data=data)
        if response_data:
            obj = PartyGroupDto(response_data, self)
            self._cache.set(PartyGroupDto, obj.id, obj)
            return obj
        return None

    def update_party_group(self, object_id: int, data: dict[str, Any]) -> PartyGroupDto | None:
        return self._put_full_update(PartyGroupDto, "/party-groups", object_id, data)

    # --- PartyGroupMembership ---
    def get_party_group_membership(self, object_id: int) -> PartyGroupMembershipDto | None:
        return self._get_object(PartyGroupMembershipDto, "/party-group-memberships", object_id)

    def get_party_group_membership_list(self) -> list[PartyGroupMembershipDto]:
        return self._get_object_list(PartyGroupMembershipDto, "/party-group-memberships/")

    def create_party_group_membership(self, data: dict[str, Any]) -> PartyGroupMembershipDto | None:
        response_data = self._make_request("/party-group-memberships/", method="POST", data=data)
        if response_data:
            obj = PartyGroupMembershipDto(response_data, self)
            self._cache.set(PartyGroupMembershipDto, obj.id, obj)
            return obj
        return None

    def update_party_group_membership(self, object_id: int, data: dict[str, Any]) -> PartyGroupMembershipDto | None:
        return self._put_full_update(PartyGroupMembershipDto, "/party-group-memberships", object_id, data)
