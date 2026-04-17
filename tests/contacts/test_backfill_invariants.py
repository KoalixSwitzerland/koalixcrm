# -*- coding: utf-8 -*-
"""Invariant tests for the legacy → Party backfill migration (issue #393).

Populates the legacy tables with a small handcrafted dataset, runs the
`forwards` function from `0005_backfill_party`, and asserts the invariants
listed in PLAN_contact_party_data_model.md §PR #2 hold on the new tables.
"""
from django.apps import apps as live_apps
from django.contrib.auth.models import User
from django.test import TestCase

from koalixcrm.contacts.backfill import forwards, reverse
from koalixcrm.contacts.models import (
    Address,
    AddressAssignment,
    EmailAssignment,
    Organization,
    OrganizationMembership,
    Party,
    PartyContact,
    PartyEmail,
    PartyGroup,
    PartyGroupMembership,
    PartyRole,
    PhoneAssignment,
    PhoneNumber,
)
from koalixcrm.contacts.models.contact import Contact as LegacyContact
from koalixcrm.contacts.models.contact import ContactPersonAssociation as LegacyContactPersonAssoc
from koalixcrm.contacts.models.contact import EmailAddressForContact as LegacyEmailAddr
from koalixcrm.contacts.models.contact import PhoneAddressForContact as LegacyPhoneAddr
from koalixcrm.contacts.models.contact import PostalAddressForContact as LegacyPostalAddr
from koalixcrm.contacts.models.customer import Customer as LegacyCustomer
from koalixcrm.contacts.models.customer_billing_cycle import CustomerBillingCycle
from koalixcrm.contacts.models.customer_group import CustomerGroup as LegacyCustomerGroup
from koalixcrm.contacts.models.person import Person as LegacyPerson
from koalixcrm.contacts.models.supplier import Supplier as LegacySupplier


class BackfillInvariantsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='migrationuser', is_staff=True)
        self.billing_cycle = CustomerBillingCycle.objects.create(
            name='Default', time_to_payment_date=30,
            payment_reminder_time_to_payment=14,
        )

        # 2 orgs: one plain Contact, one Customer, one Supplier.
        self.org_plain = LegacyContact.objects.create(name='Plain Org', last_modified_by=self.user)
        self.group = LegacyCustomerGroup.objects.create(name='Key accounts')
        self.customer = LegacyCustomer.objects.create(
            name='ACME AG', last_modified_by=self.user,
            default_customer_billing_cycle=self.billing_cycle,
            is_lead=False,
        )
        self.customer.is_member_of.add(self.group)
        self.supplier = LegacySupplier.objects.create(
            name='Supplier GmbH', last_modified_by=self.user,
            offers_shipment_to_customers=True,
        )

        # 2 natural persons. One of them works at ACME AG.
        self.person_jane = LegacyPerson.objects.create(
            name='Doe', pre_name='Jane', email='jane@example.com',
            phone='+41791111111', role='CFO',
        )
        self.person_bob = LegacyPerson.objects.create(
            name='Smith', pre_name='Bob', email='bob@example.com',
            phone='+41792222222',
        )
        LegacyContactPersonAssoc.objects.create(contact=self.customer, person=self.person_jane)

        # Postal / email / phone addresses on the customer.
        LegacyPostalAddr.objects.create(
            person=self.customer, purpose='O',
            address_line_1='Bahnhofstrasse 1', zip_code=8001, town='Zürich', country='CH',
        )
        LegacyEmailAddr.objects.create(
            person=self.customer, purpose='O', email='invoices@acme.example',
        )
        LegacyPhoneAddr.objects.create(
            person=self.customer, purpose='O', phone='+41440000000',
        )

    def test_forwards_satisfies_invariants(self):
        forwards(live_apps, None)

        legacy_contact_count = LegacyContact.objects.count()  # 3: plain + customer + supplier
        legacy_person_count = LegacyPerson.objects.count()    # 2: jane + bob

        self.assertEqual(Party.objects.count(), legacy_contact_count + legacy_person_count)
        self.assertEqual(Organization.objects.count(), legacy_contact_count)
        self.assertEqual(
            PartyRole.objects.filter(role_type='customer').count(),
            LegacyCustomer.objects.count(),
        )
        self.assertEqual(
            PartyRole.objects.filter(role_type='supplier').count(),
            LegacySupplier.objects.count(),
        )
        self.assertEqual(
            OrganizationMembership.objects.count(),
            LegacyContactPersonAssoc.objects.count(),
        )
        self.assertEqual(Address.objects.count(), 1)
        self.assertEqual(AddressAssignment.objects.count(), 1)
        # Email dedup: bob + jane + invoices@acme = 3 unique addresses.
        self.assertEqual(PartyEmail.objects.count(), 3)
        # Assignments: one per Person (jane, bob) + one on the customer = 3.
        self.assertEqual(EmailAssignment.objects.count(), 3)
        self.assertEqual(PhoneNumber.objects.count(), 3)
        self.assertEqual(PhoneAssignment.objects.count(), 3)
        self.assertEqual(PartyGroup.objects.count(), 1)
        self.assertEqual(PartyGroupMembership.objects.count(), 1)

        # Spot-check: jane's OrganizationMembership carries her role.
        membership = OrganizationMembership.objects.get()
        self.assertEqual(membership.title, 'CFO')
        self.assertEqual(
            PartyContact.objects.get(pk=membership.contact_id).family_name, 'Doe',
        )

    def test_reverse_clears_new_tables(self):
        forwards(live_apps, None)
        reverse(live_apps, None)

        self.assertEqual(Party.objects.count(), 0)
        self.assertEqual(Organization.objects.count(), 0)
        self.assertEqual(PartyContact.objects.count(), 0)
        self.assertEqual(PartyRole.objects.count(), 0)
        self.assertEqual(OrganizationMembership.objects.count(), 0)
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(AddressAssignment.objects.count(), 0)
        self.assertEqual(PartyEmail.objects.count(), 0)
        self.assertEqual(EmailAssignment.objects.count(), 0)
        self.assertEqual(PhoneNumber.objects.count(), 0)
        self.assertEqual(PhoneAssignment.objects.count(), 0)
        self.assertEqual(PartyGroup.objects.count(), 0)
        self.assertEqual(PartyGroupMembership.objects.count(), 0)

        # Legacy tables are untouched.
        self.assertEqual(LegacyContact.objects.count(), 3)
        self.assertEqual(LegacyPerson.objects.count(), 2)
