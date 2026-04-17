# -*- coding: utf-8 -*-
"""Minimal admin registrations for the new Party data model (issue #198, PR #392).

Scope: registration + list display only. Full admin UX (inlines, actions,
fieldsets) arrives in PR #394 once the new model is authoritative.
"""
from django.contrib import admin

from koalixcrm.contacts.models.party import Party
from koalixcrm.contacts.models.organization import Organization
from koalixcrm.contacts.models.natural_person import PartyContact
from koalixcrm.contacts.models.party_identification import PartyIdentification
from koalixcrm.contacts.models.party_role import PartyRole
from koalixcrm.contacts.models.organization_membership import OrganizationMembership
from koalixcrm.contacts.models.organization_relationship import OrganizationRelationship
from koalixcrm.contacts.models.address import Address
from koalixcrm.contacts.models.address_assignment import AddressAssignment
from koalixcrm.contacts.models.phone_number import PhoneNumber
from koalixcrm.contacts.models.phone_assignment import PhoneAssignment
from koalixcrm.contacts.models.party_email import PartyEmail
from koalixcrm.contacts.models.email_assignment import EmailAssignment
from koalixcrm.contacts.models.party_group import PartyGroup
from koalixcrm.contacts.models.party_group_membership import PartyGroupMembership


@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):
    list_display = ('id', 'display_name', 'default_language', 'created_at')
    search_fields = ('display_name',)


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'display_name', 'legal_form', 'legal_name', 'legal_seat_country')
    search_fields = ('display_name', 'legal_name', 'registration_number')


@admin.register(PartyContact)
class PartyContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'display_name', 'given_name', 'family_name', 'gdpr_consent_date')
    search_fields = ('display_name', 'given_name', 'family_name')


@admin.register(PartyIdentification)
class PartyIdentificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'party', 'scheme', 'value', 'valid_from', 'valid_to')
    list_filter = ('scheme',)


@admin.register(PartyRole)
class PartyRoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'party', 'role_type', 'is_primary', 'valid_from', 'valid_to')
    list_filter = ('role_type', 'is_primary')


@admin.register(OrganizationMembership)
class OrganizationMembershipAdmin(admin.ModelAdmin):
    list_display = ('id', 'contact', 'organization', 'title', 'position', 'is_primary')
    list_filter = ('is_primary',)


@admin.register(OrganizationRelationship)
class OrganizationRelationshipAdmin(admin.ModelAdmin):
    list_display = ('id', 'parent', 'child', 'relationship_type', 'valid_from', 'valid_to')
    list_filter = ('relationship_type',)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'address_line_1', 'zip_code', 'town', 'country')
    search_fields = ('address_line_1', 'zip_code', 'town')


@admin.register(AddressAssignment)
class AddressAssignmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'party', 'address', 'purpose', 'is_primary', 'valid_from', 'valid_to')
    list_filter = ('purpose', 'is_primary')


@admin.register(PhoneNumber)
class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone_e164')
    search_fields = ('phone_e164',)


@admin.register(PhoneAssignment)
class PhoneAssignmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'party', 'phone', 'purpose', 'is_primary')
    list_filter = ('purpose', 'is_primary')


@admin.register(PartyEmail)
class PartyEmailAdmin(admin.ModelAdmin):
    list_display = ('id', 'email')
    search_fields = ('email',)


@admin.register(EmailAssignment)
class EmailAssignmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'party', 'email', 'purpose', 'is_primary')
    list_filter = ('purpose', 'is_primary')


@admin.register(PartyGroup)
class PartyGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'role_type_scope')
    list_filter = ('role_type_scope',)
    search_fields = ('name',)


@admin.register(PartyGroupMembership)
class PartyGroupMembershipAdmin(admin.ModelAdmin):
    list_display = ('id', 'party', 'party_group')
