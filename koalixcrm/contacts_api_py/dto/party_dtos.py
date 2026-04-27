# -*- coding: utf-8 -*-
"""Python DTOs for the Party data model (issue #394 Phase E).

One class per REST resource registered by `projectsettings/urls.py`
under /api/parties, /api/organizations, etc. Attributes mirror the
field lists in `koalixcrm.contacts.serializers.party_serializers`.

Consolidated into a single module (rather than one file per class,
as the legacy DTOs did) because they are value-object shells with
no custom behaviour.
"""
from typing import Any, Dict

from koalixcrm.shared.base_model import BaseModel


class Party(BaseModel):
    def __init__(self, data: Dict[str, Any], client=None):
        self.display_name = None
        self.default_language = None
        self.created_at = None
        self.updated_at = None
        self.last_modified_by = None
        super().__init__(data)


class Organization(BaseModel):
    def __init__(self, data: Dict[str, Any], client=None):
        self.display_name = None
        self.default_language = None
        self.legal_form = None
        self.legal_name = None
        self.registration_number = None
        self.legal_seat_country = None
        self.created_at = None
        self.updated_at = None
        super().__init__(data)


class PartyContact(BaseModel):
    """Natural-person Party (transitional name — see ADR 0001)."""

    def __init__(self, data: Dict[str, Any], client=None):
        self.display_name = None
        self.default_language = None
        self.prefix = None
        self.given_name = None
        self.family_name = None
        self.date_of_birth = None
        self.gdpr_consent_date = None
        self.created_at = None
        self.updated_at = None
        super().__init__(data)


class PartyIdentification(BaseModel):
    def __init__(self, data: Dict[str, Any], client=None):
        self.party = None
        self.scheme = None
        self.value = None
        self.valid_from = None
        self.valid_to = None
        super().__init__(data)


class PartyRole(BaseModel):
    def __init__(self, data: Dict[str, Any], client=None):
        self.party = None
        self.role_type = None
        self.is_primary = None
        self.valid_from = None
        self.valid_to = None
        super().__init__(data)


class OrganizationMembership(BaseModel):
    def __init__(self, data: Dict[str, Any], client=None):
        self.contact = None
        self.organization = None
        self.title = None
        self.position = None
        self.is_primary = None
        self.valid_from = None
        self.valid_to = None
        super().__init__(data)


class OrganizationRelationship(BaseModel):
    def __init__(self, data: Dict[str, Any], client=None):
        self.parent = None
        self.child = None
        self.relationship_type = None
        self.valid_from = None
        self.valid_to = None
        super().__init__(data)


class Address(BaseModel):
    def __init__(self, data: Dict[str, Any], client=None):
        self.street = None
        self.number = None
        self.additional_address_line_1 = None
        self.additional_address_line_2 = None
        self.additional_address_line_3 = None
        self.zip_code = None
        self.town = None
        self.state = None
        self.country = None
        self.subdivision_code = None
        super().__init__(data)


class AddressAssignment(BaseModel):
    def __init__(self, data: Dict[str, Any], client=None):
        self.party = None
        self.address = None
        self.purpose = None
        self.is_primary = None
        self.valid_from = None
        self.valid_to = None
        super().__init__(data)


class PhoneNumber(BaseModel):
    def __init__(self, data: Dict[str, Any], client=None):
        self.phone_e164 = None
        super().__init__(data)


class PhoneAssignment(BaseModel):
    def __init__(self, data: Dict[str, Any], client=None):
        self.party = None
        self.phone = None
        self.purpose = None
        self.is_primary = None
        self.valid_from = None
        self.valid_to = None
        super().__init__(data)


class PartyEmail(BaseModel):
    def __init__(self, data: Dict[str, Any], client=None):
        self.email = None
        super().__init__(data)


class EmailAssignment(BaseModel):
    def __init__(self, data: Dict[str, Any], client=None):
        self.party = None
        self.email = None
        self.purpose = None
        self.is_primary = None
        self.valid_from = None
        self.valid_to = None
        super().__init__(data)


class PartyGroup(BaseModel):
    def __init__(self, data: Dict[str, Any], client=None):
        self.name = None
        self.role_type_scope = None
        super().__init__(data)


class PartyGroupMembership(BaseModel):
    def __init__(self, data: Dict[str, Any], client=None):
        self.party = None
        self.party_group = None
        super().__init__(data)
