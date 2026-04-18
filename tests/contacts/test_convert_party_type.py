# -*- coding: utf-8 -*-
"""Round-trip test for the bulk admin actions that flip a Party's
MTI-child between Organization and natural-person Contact (issue #395).
"""
from datetime import date
from unittest.mock import MagicMock

from django.test import TestCase

from koalixcrm.contacts.admin.actions import (
    convert_contacts_to_organizations,
    convert_organizations_to_contacts,
)
from koalixcrm.contacts.models.address import Address
from koalixcrm.contacts.models.address_assignment import AddressAssignment
from koalixcrm.contacts.models.natural_person import PartyContact
from koalixcrm.contacts.models.organization import Organization
from koalixcrm.contacts.models.organization_membership import OrganizationMembership
from koalixcrm.contacts.models.party import Party
from koalixcrm.contacts.models.party_role import PartyRole


class ConvertOrganizationToContactTest(TestCase):
    def setUp(self):
        self.org = Organization.objects.create(
            display_name='Jane Doe',
            legal_name='Jane Doe',
        )
        self.address = Address.objects.create(
            address_line_1='Bahnhofstrasse 1', zip_code='8001',
            town='Zürich', country='CH',
        )
        self.assignment = AddressAssignment.objects.create(
            party=self.org.party_ptr, address=self.address,
            purpose='billing', is_primary=True,
            valid_from=date(1970, 1, 1),
        )
        self.role = PartyRole.objects.create(
            party=self.org.party_ptr, role_type='customer',
            is_primary=True, valid_from=date(1970, 1, 1),
        )

    def _run_action(self, queryset):
        modeladmin = MagicMock()
        request = MagicMock()
        convert_organizations_to_contacts(modeladmin, request, queryset)
        return modeladmin.message_user.call_args

    def test_conversion_preserves_party_and_assignments(self):
        party_id = self.org.pk
        self._run_action(Organization.objects.filter(pk=party_id))

        self.assertFalse(Organization.objects.filter(pk=party_id).exists())
        self.assertTrue(PartyContact.objects.filter(pk=party_id).exists())
        # Party row intact — same id, same display_name.
        self.assertTrue(Party.objects.filter(pk=party_id, display_name='Jane Doe').exists())
        # PartyRole, AddressAssignment, Address all survive.
        self.assertTrue(PartyRole.objects.filter(pk=self.role.pk).exists())
        self.assertTrue(AddressAssignment.objects.filter(pk=self.assignment.pk).exists())
        self.assertTrue(Address.objects.filter(pk=self.address.pk).exists())

        contact = PartyContact.objects.get(pk=party_id)
        self.assertEqual(contact.given_name, 'Jane')
        self.assertEqual(contact.family_name, 'Doe')

    def test_single_word_name_lands_in_family_name(self):
        org = Organization.objects.create(display_name='Madonna')
        self._run_action(Organization.objects.filter(pk=org.pk))
        contact = PartyContact.objects.get(pk=org.pk)
        self.assertEqual(contact.given_name, '')
        self.assertEqual(contact.family_name, 'Madonna')

    def test_memberships_are_removed(self):
        employee = PartyContact.objects.create(
            display_name='Bob', given_name='Bob', family_name='',
        )
        OrganizationMembership.objects.create(
            contact=employee, organization=self.org, title='CFO',
        )
        self._run_action(Organization.objects.filter(pk=self.org.pk))
        self.assertFalse(OrganizationMembership.objects.filter(
            organization_id=self.org.pk,
        ).exists())

    def test_already_converted_party_is_skipped(self):
        # Manually wedge a PartyContact child row onto the same Party id via
        # raw SQL — this is the anomaly where the same party happens to be
        # both an Organization and a PartyContact. The action must detect it
        # and skip so we don't double-convert.
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute(
                'INSERT INTO crm_partycontact '
                '(party_ptr_id, given_name, family_name) VALUES (%s, %s, %s)',
                [self.org.pk, 'Existing', 'Record'],
            )
        self._run_action(Organization.objects.filter(pk=self.org.pk))
        self.assertTrue(Organization.objects.filter(pk=self.org.pk).exists())


class ConvertContactToOrganizationTest(TestCase):
    def test_round_trip(self):
        contact = PartyContact.objects.create(
            display_name='Evil Corp',
            given_name='Evil', family_name='Corp',
        )
        modeladmin = MagicMock()
        request = MagicMock()
        convert_contacts_to_organizations(
            modeladmin, request,
            PartyContact.objects.filter(pk=contact.pk),
        )
        self.assertFalse(PartyContact.objects.filter(pk=contact.pk).exists())
        self.assertTrue(Organization.objects.filter(pk=contact.pk).exists())
        org = Organization.objects.get(pk=contact.pk)
        self.assertEqual(org.legal_name, 'Evil Corp')
        self.assertEqual(org.display_name, 'Evil Corp')
