# -*- coding: utf-8 -*-
"""Model-level tests for the new Party data model (issue #198, PR #392).

Scope per PLAN_contact_party_data_model.md §PR #1 acceptance criteria:
create + save + __str__ for every new model. Relationship integrity
(cascades, constraints) is intentionally out of scope here — covered
later once the model is authoritative.
"""
import datetime

from django.test import TestCase

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
from koalixcrm.core.models.workspace import Workspace


class PartyModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.ws, _ = Workspace.objects.get_or_create(name='Default Workspace', defaults={'is_active': True})

    def test_party_create(self):
        party = Party.objects.create(display_name="ACME AG", workspace=self.ws)
        self.assertIsNotNone(party.id)
        self.assertEqual(str(party), "ACME AG")
        self.assertIsNotNone(party.created_at)
        self.assertIsNotNone(party.updated_at)


class OrganizationModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.ws, _ = Workspace.objects.get_or_create(name='Default Workspace', defaults={'is_active': True})

    def test_organization_create_and_str_inherits_display_name(self):
        org = Organization.objects.create(
            display_name="ACME AG",
            legal_form='ag',
            legal_name="ACME Aktiengesellschaft",
            registration_number="CHE-123.456.789",
            legal_seat_country='CH',
            workspace=self.ws,
        )
        self.assertIsNotNone(org.id)
        self.assertIsNotNone(org.party_ptr_id)
        self.assertEqual(str(org), "ACME AG")
        self.assertEqual(Party.objects.count(), 1)


class PartyContactModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.ws, _ = Workspace.objects.get_or_create(name='Default Workspace', defaults={'is_active': True})

    def test_party_contact_create(self):
        contact = PartyContact.objects.create(
            display_name="Jane Doe",
            given_name="Jane",
            family_name="Doe",
            date_of_birth=datetime.date(1990, 1, 1),
            default_language='en',
            workspace=self.ws,
        )
        self.assertIsNotNone(contact.id)
        self.assertEqual(str(contact), "Jane Doe")


class PartyIdentificationModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.ws, _ = Workspace.objects.get_or_create(name='Default Workspace', defaults={'is_active': True})

    def test_party_identification_create(self):
        party = Party.objects.create(display_name="ACME AG", workspace=self.ws)
        ident = PartyIdentification.objects.create(
            party=party,
            scheme='uid',
            value='CHE-123.456.789',
            workspace=self.ws,
        )
        self.assertEqual(str(ident), "uid:CHE-123.456.789")


class PartyRoleModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.ws, _ = Workspace.objects.get_or_create(name='Default Workspace', defaults={'is_active': True})

    def test_party_role_create(self):
        party = Party.objects.create(display_name="ACME AG", workspace=self.ws)
        role = PartyRole.objects.create(
            party=party,
            role_type='customer',
            is_primary=True,
            valid_from=datetime.date(2020, 1, 1),
            workspace=self.ws,
        )
        self.assertIn("customer", str(role))


class OrganizationMembershipModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.ws, _ = Workspace.objects.get_or_create(name='Default Workspace', defaults={'is_active': True})

    def test_membership_create(self):
        org = Organization.objects.create(display_name="ACME AG", workspace=self.ws)
        contact = PartyContact.objects.create(
            display_name="Jane Doe", given_name="Jane", family_name="Doe", workspace=self.ws,
        )
        membership = OrganizationMembership.objects.create(
            contact=contact,
            organization=org,
            title="CFO",
            position="Executive",
            is_primary=True,
            workspace=self.ws,
        )
        self.assertIn("@", str(membership))


class OrganizationRelationshipModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.ws, _ = Workspace.objects.get_or_create(name='Default Workspace', defaults={'is_active': True})

    def test_relationship_create(self):
        parent = Organization.objects.create(display_name="Holding AG", workspace=self.ws)
        child = Organization.objects.create(display_name="ACME AG", workspace=self.ws)
        rel = OrganizationRelationship.objects.create(
            parent=parent, child=child, relationship_type='parent_of', workspace=self.ws,
        )
        self.assertIn("parent_of", str(rel))


class AddressModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.ws, _ = Workspace.objects.get_or_create(name='Default Workspace', defaults={'is_active': True})

    def test_address_create(self):
        addr = Address.objects.create(
            address_line_1="Bahnhofstrasse 1",
            zip_code="8001",
            town="Zürich",
            country='CH',
            subdivision_code='ZH',
            workspace=self.ws,
        )
        self.assertIn("Zürich", str(addr))


class AddressAssignmentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.ws, _ = Workspace.objects.get_or_create(name='Default Workspace', defaults={'is_active': True})

    def test_address_assignment_create(self):
        party = Party.objects.create(display_name="ACME AG", workspace=self.ws)
        addr = Address.objects.create(
            address_line_1="Bahnhofstrasse 1", zip_code="8001", town="Zürich", country='CH',
            workspace=self.ws,
        )
        assignment = AddressAssignment.objects.create(
            party=party, address=addr, purpose='billing', is_primary=True, workspace=self.ws,
        )
        self.assertIn("billing", str(assignment))


class PhoneNumberModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.ws, _ = Workspace.objects.get_or_create(name='Default Workspace', defaults={'is_active': True})

    def test_phone_create(self):
        phone = PhoneNumber.objects.create(phone_e164="+41791234567", workspace=self.ws)
        self.assertEqual(str(phone), "+41791234567")


class PhoneAssignmentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.ws, _ = Workspace.objects.get_or_create(name='Default Workspace', defaults={'is_active': True})

    def test_phone_assignment_create(self):
        party = Party.objects.create(display_name="ACME AG", workspace=self.ws)
        phone = PhoneNumber.objects.create(phone_e164="+41791234567", workspace=self.ws)
        assignment = PhoneAssignment.objects.create(
            party=party, phone=phone, purpose='primary', workspace=self.ws,
        )
        self.assertIn("primary", str(assignment))


class PartyEmailModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.ws, _ = Workspace.objects.get_or_create(name='Default Workspace', defaults={'is_active': True})

    def test_party_email_create(self):
        email = PartyEmail.objects.create(email="hello@example.com", workspace=self.ws)
        self.assertEqual(str(email), "hello@example.com")


class EmailAssignmentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.ws, _ = Workspace.objects.get_or_create(name='Default Workspace', defaults={'is_active': True})

    def test_email_assignment_create(self):
        party = Party.objects.create(display_name="ACME AG", workspace=self.ws)
        email = PartyEmail.objects.create(email="hello@example.com", workspace=self.ws)
        assignment = EmailAssignment.objects.create(
            party=party, email=email, purpose='billing', workspace=self.ws,
        )
        self.assertIn("billing", str(assignment))


class PartyGroupModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.ws, _ = Workspace.objects.get_or_create(name='Default Workspace', defaults={'is_active': True})

    def test_party_group_create(self):
        group = PartyGroup.objects.create(
            name="Key accounts", role_type_scope='customer', workspace=self.ws,
        )
        self.assertEqual(str(group), "Key accounts")


class PartyGroupMembershipModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.ws, _ = Workspace.objects.get_or_create(name='Default Workspace', defaults={'is_active': True})

    def test_membership_create(self):
        party = Party.objects.create(display_name="ACME AG", workspace=self.ws)
        group = PartyGroup.objects.create(
            name="Key accounts", role_type_scope='customer', workspace=self.ws,
        )
        m = PartyGroupMembership.objects.create(party=party, party_group=group, workspace=self.ws)
        self.assertIn("@", str(m))
