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


class PartyModelTest(TestCase):
    def test_party_create(self):
        party = Party.objects.create(display_name="ACME AG")
        self.assertIsNotNone(party.id)
        self.assertEqual(str(party), "ACME AG")
        self.assertIsNotNone(party.created_at)
        self.assertIsNotNone(party.updated_at)


class OrganizationModelTest(TestCase):
    def test_organization_create_and_str_inherits_display_name(self):
        org = Organization.objects.create(
            display_name="ACME AG",
            legal_form='ag',
            legal_name="ACME Aktiengesellschaft",
            registration_number="CHE-123.456.789",
            legal_seat_country='CH',
        )
        self.assertIsNotNone(org.id)
        self.assertIsNotNone(org.party_ptr_id)
        self.assertEqual(str(org), "ACME AG")
        self.assertEqual(Party.objects.count(), 1)


class PartyContactModelTest(TestCase):
    def test_party_contact_create(self):
        contact = PartyContact.objects.create(
            display_name="Jane Doe",
            given_name="Jane",
            family_name="Doe",
            date_of_birth=datetime.date(1990, 1, 1),
            default_language='en',
        )
        self.assertIsNotNone(contact.id)
        self.assertEqual(str(contact), "Jane Doe")


class PartyIdentificationModelTest(TestCase):
    def test_party_identification_create(self):
        party = Party.objects.create(display_name="ACME AG")
        ident = PartyIdentification.objects.create(
            party=party,
            scheme='uid',
            value='CHE-123.456.789',
        )
        self.assertEqual(str(ident), "uid:CHE-123.456.789")


class PartyRoleModelTest(TestCase):
    def test_party_role_create(self):
        party = Party.objects.create(display_name="ACME AG")
        role = PartyRole.objects.create(
            party=party,
            role_type='customer',
            is_primary=True,
            valid_from=datetime.date(2020, 1, 1),
        )
        self.assertIn("customer", str(role))


class OrganizationMembershipModelTest(TestCase):
    def test_membership_create(self):
        org = Organization.objects.create(display_name="ACME AG")
        contact = PartyContact.objects.create(display_name="Jane Doe", given_name="Jane", family_name="Doe")
        membership = OrganizationMembership.objects.create(
            contact=contact,
            organization=org,
            title="CFO",
            position="Executive",
            is_primary=True,
        )
        self.assertIn("@", str(membership))


class OrganizationRelationshipModelTest(TestCase):
    def test_relationship_create(self):
        parent = Organization.objects.create(display_name="Holding AG")
        child = Organization.objects.create(display_name="ACME AG")
        rel = OrganizationRelationship.objects.create(
            parent=parent, child=child, relationship_type='parent_of',
        )
        self.assertIn("parent_of", str(rel))


class AddressModelTest(TestCase):
    def test_address_create(self):
        addr = Address.objects.create(
            address_line_1="Bahnhofstrasse 1",
            zip_code="8001",
            town="Zürich",
            country='CH',
            subdivision_code='ZH',
        )
        self.assertIn("Zürich", str(addr))


class AddressAssignmentModelTest(TestCase):
    def test_address_assignment_create(self):
        party = Party.objects.create(display_name="ACME AG")
        addr = Address.objects.create(address_line_1="Bahnhofstrasse 1", zip_code="8001", town="Zürich", country='CH')
        assignment = AddressAssignment.objects.create(
            party=party, address=addr, purpose='billing', is_primary=True,
        )
        self.assertIn("billing", str(assignment))


class PhoneNumberModelTest(TestCase):
    def test_phone_create(self):
        phone = PhoneNumber.objects.create(phone_e164="+41791234567")
        self.assertEqual(str(phone), "+41791234567")


class PhoneAssignmentModelTest(TestCase):
    def test_phone_assignment_create(self):
        party = Party.objects.create(display_name="ACME AG")
        phone = PhoneNumber.objects.create(phone_e164="+41791234567")
        assignment = PhoneAssignment.objects.create(
            party=party, phone=phone, purpose='primary',
        )
        self.assertIn("primary", str(assignment))


class PartyEmailModelTest(TestCase):
    def test_party_email_create(self):
        email = PartyEmail.objects.create(email="hello@example.com")
        self.assertEqual(str(email), "hello@example.com")


class EmailAssignmentModelTest(TestCase):
    def test_email_assignment_create(self):
        party = Party.objects.create(display_name="ACME AG")
        email = PartyEmail.objects.create(email="hello@example.com")
        assignment = EmailAssignment.objects.create(
            party=party, email=email, purpose='billing',
        )
        self.assertIn("billing", str(assignment))


class PartyGroupModelTest(TestCase):
    def test_party_group_create(self):
        group = PartyGroup.objects.create(name="Key accounts", role_type_scope='customer')
        self.assertEqual(str(group), "Key accounts")


class PartyGroupMembershipModelTest(TestCase):
    def test_membership_create(self):
        party = Party.objects.create(display_name="ACME AG")
        group = PartyGroup.objects.create(name="Key accounts", role_type_scope='customer')
        m = PartyGroupMembership.objects.create(party=party, party_group=group)
        self.assertIn("@", str(m))
