# -*- coding: utf-8 -*-
"""DRF viewsets for the new Party data model (issue #394)."""
from koalixcrm.shared.base_model_view_set import BaseModelViewSet

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
from koalixcrm.contacts.serializers.party_serializers import (
    AddressAssignmentJSONSerializer,
    AddressJSONSerializer,
    EmailAssignmentJSONSerializer,
    OrganizationJSONSerializer,
    OrganizationMembershipJSONSerializer,
    OrganizationRelationshipJSONSerializer,
    PartyContactJSONSerializer,
    PartyEmailJSONSerializer,
    PartyGroupJSONSerializer,
    PartyGroupMembershipJSONSerializer,
    PartyIdentificationJSONSerializer,
    PartyJSONSerializer,
    PartyRoleJSONSerializer,
    PhoneAssignmentJSONSerializer,
    PhoneNumberJSONSerializer,
)


class PartyViewSet(BaseModelViewSet):
    queryset = Party.objects.all()
    serializer_class = PartyJSONSerializer


class OrganizationViewSet(BaseModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationJSONSerializer


class PartyContactViewSet(BaseModelViewSet):
    queryset = PartyContact.objects.all()
    serializer_class = PartyContactJSONSerializer


class PartyIdentificationViewSet(BaseModelViewSet):
    queryset = PartyIdentification.objects.all()
    serializer_class = PartyIdentificationJSONSerializer


class PartyRoleViewSet(BaseModelViewSet):
    queryset = PartyRole.objects.all()
    serializer_class = PartyRoleJSONSerializer


class OrganizationMembershipViewSet(BaseModelViewSet):
    queryset = OrganizationMembership.objects.all()
    serializer_class = OrganizationMembershipJSONSerializer


class OrganizationRelationshipViewSet(BaseModelViewSet):
    queryset = OrganizationRelationship.objects.all()
    serializer_class = OrganizationRelationshipJSONSerializer


class AddressViewSet(BaseModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressJSONSerializer


class AddressAssignmentViewSet(BaseModelViewSet):
    queryset = AddressAssignment.objects.all()
    serializer_class = AddressAssignmentJSONSerializer


class PhoneNumberViewSet(BaseModelViewSet):
    queryset = PhoneNumber.objects.all()
    serializer_class = PhoneNumberJSONSerializer


class PhoneAssignmentViewSet(BaseModelViewSet):
    queryset = PhoneAssignment.objects.all()
    serializer_class = PhoneAssignmentJSONSerializer


class PartyEmailViewSet(BaseModelViewSet):
    queryset = PartyEmail.objects.all()
    serializer_class = PartyEmailJSONSerializer


class EmailAssignmentViewSet(BaseModelViewSet):
    queryset = EmailAssignment.objects.all()
    serializer_class = EmailAssignmentJSONSerializer


class PartyGroupViewSet(BaseModelViewSet):
    queryset = PartyGroup.objects.all()
    serializer_class = PartyGroupJSONSerializer


class PartyGroupMembershipViewSet(BaseModelViewSet):
    queryset = PartyGroupMembership.objects.all()
    serializer_class = PartyGroupMembershipJSONSerializer
