# -*- coding: utf-8 -*-
"""Minimal admin registrations for the new Party data model (issue #198, PR #392).

Scope: registration + list display only. Full admin UX (inlines, actions,
fieldsets) arrives in PR #394 once the new model is authoritative.
"""
from __future__ import annotations

from django.contrib import admin

from koalixcrm.contacts.admin.actions import (
    convert_contacts_to_organizations,
    convert_organizations_to_contacts,
)
from koalixcrm.contacts.models.address import Address
from koalixcrm.contacts.models.address_assignment import AddressAssignment
from koalixcrm.contacts.models.email_assignment import EmailAssignment
from koalixcrm.contacts.models.natural_person import PartyContact
from koalixcrm.contacts.models.organization import Organization
from koalixcrm.contacts.models.organization_membership import OrganizationMembership
from koalixcrm.contacts.models.organization_relationship import OrganizationRelationship
from koalixcrm.contacts.models.party import Party
from koalixcrm.contacts.models.party_email import PartyEmail
from koalixcrm.contacts.models.party_group import PartyGroup
from koalixcrm.contacts.models.party_group_membership import PartyGroupMembership
from koalixcrm.contacts.models.party_identification import PartyIdentification
from koalixcrm.contacts.models.party_role import PartyRole
from koalixcrm.contacts.models.phone_assignment import PhoneAssignment
from koalixcrm.contacts.models.phone_number import PhoneNumber
from koalixcrm.core.admin.workspace_scoped_admin import WorkspaceScopedModelAdmin


@admin.register(Party)
class PartyAdmin(WorkspaceScopedModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'display_name', 'default_language', 'created_at')
    list_filter = ('workspace',)
    search_fields = ('display_name',)


@admin.register(Organization)
class OrganizationAdmin(WorkspaceScopedModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'display_name', 'legal_form', 'legal_name', 'legal_seat_country')
    list_filter = ('workspace',)
    search_fields = ('display_name', 'legal_name', 'registration_number')
    actions = [convert_organizations_to_contacts]


@admin.register(PartyContact)
class PartyContactAdmin(WorkspaceScopedModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'display_name', 'given_name', 'family_name', 'gdpr_consent_date')
    list_filter = ('workspace',)
    search_fields = ('display_name', 'given_name', 'family_name')
    actions = [convert_contacts_to_organizations]


@admin.register(PartyIdentification)
class PartyIdentificationAdmin(WorkspaceScopedModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'party', 'scheme', 'value', 'valid_from', 'valid_to')
    list_filter = ('scheme', 'workspace')


@admin.register(PartyRole)
class PartyRoleAdmin(WorkspaceScopedModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'party', 'role_type', 'is_primary', 'valid_from', 'valid_to')
    list_filter = ('role_type', 'is_primary', 'workspace')


@admin.register(OrganizationMembership)
class OrganizationMembershipAdmin(WorkspaceScopedModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'contact', 'organization', 'title', 'position', 'is_primary')
    list_filter = ('is_primary', 'workspace')


@admin.register(OrganizationRelationship)
class OrganizationRelationshipAdmin(WorkspaceScopedModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'parent', 'child', 'relationship_type', 'valid_from', 'valid_to')
    list_filter = ('relationship_type', 'workspace')


@admin.register(Address)
class AddressAdmin(WorkspaceScopedModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'street', 'zip_code', 'town', 'country')
    list_filter = ('workspace',)
    search_fields = ('street', 'zip_code', 'town')


@admin.register(AddressAssignment)
class AddressAssignmentAdmin(WorkspaceScopedModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'party', 'address', 'purpose', 'is_primary', 'valid_from', 'valid_to')
    list_filter = ('purpose', 'is_primary', 'workspace')


@admin.register(PhoneNumber)
class PhoneNumberAdmin(WorkspaceScopedModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'phone_e164')
    list_filter = ('workspace',)
    search_fields = ('phone_e164',)


@admin.register(PhoneAssignment)
class PhoneAssignmentAdmin(WorkspaceScopedModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'party', 'phone', 'purpose', 'is_primary')
    list_filter = ('purpose', 'is_primary', 'workspace')


@admin.register(PartyEmail)
class PartyEmailAdmin(WorkspaceScopedModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'email')
    list_filter = ('workspace',)
    search_fields = ('email',)


@admin.register(EmailAssignment)
class EmailAssignmentAdmin(WorkspaceScopedModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'party', 'email', 'purpose', 'is_primary')
    list_filter = ('purpose', 'is_primary', 'workspace')


@admin.register(PartyGroup)
class PartyGroupAdmin(WorkspaceScopedModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'name', 'role_type_scope')
    list_filter = ('role_type_scope', 'workspace')
    search_fields = ('name',)


@admin.register(PartyGroupMembership)
class PartyGroupMembershipAdmin(WorkspaceScopedModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'party', 'party_group')
    list_filter = ('workspace',)
