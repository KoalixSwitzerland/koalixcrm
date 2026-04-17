# -*- coding: utf-8 -*-
"""DRF serializers for the new Party data model (issue #394).

Minimal ModelSerializer layer — nested / custom create/update behaviour is
deferred until the API shape is agreed. All 15 new models are exposed as
flat JSON resources; relationships are serialized as IDs.
"""
from rest_framework import serializers

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


class PartyJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = Party
        fields = (
            'id', 'display_name', 'default_language',
            'created_at', 'updated_at', 'last_modified_by',
        )
        read_only_fields = ('created_at', 'updated_at')


class OrganizationJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = (
            'id', 'display_name', 'default_language',
            'legal_form', 'legal_name',
            'registration_number', 'legal_seat_country',
            'created_at', 'updated_at',
        )
        read_only_fields = ('created_at', 'updated_at')


class PartyContactJSONSerializer(serializers.ModelSerializer):
    """Serializer for the natural-person Party (PartyContact, transitional name)."""
    class Meta:
        model = PartyContact
        fields = (
            'id', 'display_name', 'default_language',
            'prefix', 'given_name', 'family_name',
            'date_of_birth', 'gdpr_consent_date', 'preferred_language',
            'created_at', 'updated_at',
        )
        read_only_fields = ('created_at', 'updated_at')


class PartyIdentificationJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartyIdentification
        fields = ('id', 'party', 'scheme', 'value', 'valid_from', 'valid_to')


class PartyRoleJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartyRole
        fields = ('id', 'party', 'role_type', 'is_primary', 'valid_from', 'valid_to')


class OrganizationMembershipJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationMembership
        fields = (
            'id', 'contact', 'organization', 'title', 'position',
            'is_primary', 'valid_from', 'valid_to',
        )


class OrganizationRelationshipJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationRelationship
        fields = (
            'id', 'parent', 'child', 'relationship_type',
            'valid_from', 'valid_to',
        )


class AddressJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = (
            'id',
            'address_line_1', 'address_line_2', 'address_line_3', 'address_line_4',
            'zip_code', 'town', 'state', 'country', 'subdivision_code',
        )


class AddressAssignmentJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressAssignment
        fields = ('id', 'party', 'address', 'purpose', 'is_primary', 'valid_from', 'valid_to')


class PhoneNumberJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = ('id', 'phone_e164')


class PhoneAssignmentJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneAssignment
        fields = ('id', 'party', 'phone', 'purpose', 'is_primary', 'valid_from', 'valid_to')


class PartyEmailJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartyEmail
        fields = ('id', 'email')


class EmailAssignmentJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailAssignment
        fields = ('id', 'party', 'email', 'purpose', 'is_primary', 'valid_from', 'valid_to')


class PartyGroupJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartyGroup
        fields = ('id', 'name', 'role_type_scope')


class PartyGroupMembershipJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartyGroupMembership
        fields = ('id', 'party', 'party_group')
