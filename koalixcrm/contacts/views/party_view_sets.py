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


class WorkspaceScopedViewSetMixin:
    """Filter queryset by active_workspace; stamp workspace on create."""

    def get_queryset(self):
        qs = super().get_queryset()
        active = getattr(self.request, 'active_workspace', None)
        if active is not None:
            return qs.filter(workspace=active)
        if not self.request.user.is_superuser:
            return qs.none()
        return qs

    def perform_create(self, serializer):
        from koalixcrm.core.models.workspace import Workspace
        active = getattr(self.request, 'active_workspace', None)
        if active is None and self.request.user.is_superuser:
            active, _ = Workspace.objects.get_or_create(
                name='Default Workspace', defaults={'is_active': True}
            )
        serializer.save(workspace=active)


class PartyViewSet(WorkspaceScopedViewSetMixin, BaseModelViewSet):
    queryset = Party.objects.all()
    serializer_class = PartyJSONSerializer


class OrganizationViewSet(WorkspaceScopedViewSetMixin, BaseModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationJSONSerializer


class PartyContactViewSet(WorkspaceScopedViewSetMixin, BaseModelViewSet):
    queryset = PartyContact.objects.all()
    serializer_class = PartyContactJSONSerializer


class PartyIdentificationViewSet(WorkspaceScopedViewSetMixin, BaseModelViewSet):
    queryset = PartyIdentification.objects.all()
    serializer_class = PartyIdentificationJSONSerializer


class PartyRoleViewSet(WorkspaceScopedViewSetMixin, BaseModelViewSet):
    queryset = PartyRole.objects.all()
    serializer_class = PartyRoleJSONSerializer


class OrganizationMembershipViewSet(WorkspaceScopedViewSetMixin, BaseModelViewSet):
    queryset = OrganizationMembership.objects.all()
    serializer_class = OrganizationMembershipJSONSerializer


class OrganizationRelationshipViewSet(WorkspaceScopedViewSetMixin, BaseModelViewSet):
    queryset = OrganizationRelationship.objects.all()
    serializer_class = OrganizationRelationshipJSONSerializer


class AddressViewSet(WorkspaceScopedViewSetMixin, BaseModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressJSONSerializer


class AddressAssignmentViewSet(WorkspaceScopedViewSetMixin, BaseModelViewSet):
    queryset = AddressAssignment.objects.all()
    serializer_class = AddressAssignmentJSONSerializer


class PhoneNumberViewSet(WorkspaceScopedViewSetMixin, BaseModelViewSet):
    queryset = PhoneNumber.objects.all()
    serializer_class = PhoneNumberJSONSerializer


class PhoneAssignmentViewSet(WorkspaceScopedViewSetMixin, BaseModelViewSet):
    queryset = PhoneAssignment.objects.all()
    serializer_class = PhoneAssignmentJSONSerializer


class PartyEmailViewSet(WorkspaceScopedViewSetMixin, BaseModelViewSet):
    queryset = PartyEmail.objects.all()
    serializer_class = PartyEmailJSONSerializer


class EmailAssignmentViewSet(WorkspaceScopedViewSetMixin, BaseModelViewSet):
    queryset = EmailAssignment.objects.all()
    serializer_class = EmailAssignmentJSONSerializer


class PartyGroupViewSet(WorkspaceScopedViewSetMixin, BaseModelViewSet):
    queryset = PartyGroup.objects.all()
    serializer_class = PartyGroupJSONSerializer


class PartyGroupMembershipViewSet(WorkspaceScopedViewSetMixin, BaseModelViewSet):
    queryset = PartyGroupMembership.objects.all()
    serializer_class = PartyGroupMembershipJSONSerializer
