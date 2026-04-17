# -*- coding: utf-8 -*-
"""Forward / reverse logic for the legacy-to-Party backfill.

Kept as a standalone module (rather than inlined into the migration file) so
tests and management commands can call it directly — migration filenames
start with a digit and aren't valid Python module names for import.

Both functions accept Django's `apps` registry and a `schema_editor`. The
migration passes its historical `apps` + the schema editor; tests and
management commands pass `django.apps.apps` + `None`. Either works because
the code only uses `apps.get_model(...)`.

See PLAN_contact_party_data_model.md §PR #2, issue #393.
"""
import datetime


EPOCH = datetime.date(1970, 1, 1)


_LEGACY_PURPOSE_MAP = {
    'H': 'other',    # Private
    'O': 'billing',  # Business
    'P': 'other',    # Mobile Private — only meaningful for phone
    'B': 'billing',  # Mobile Business — only meaningful for phone
}


def _map_purpose(legacy_code):
    if not legacy_code:
        return 'other'
    return _LEGACY_PURPOSE_MAP.get(legacy_code, 'other')


def _addr_key(row):
    return (
        row.address_line_1 or '',
        row.address_line_2 or '',
        row.address_line_3 or '',
        row.address_line_4 or '',
        row.zip_code,
        row.town or '',
        row.state or '',
        row.country or '',
        row.subdivision_code or '',
    )


def forwards(apps, schema_editor):
    LegacyContact = apps.get_model('contacts', 'Contact')
    LegacyCustomer = apps.get_model('contacts', 'Customer')
    LegacySupplier = apps.get_model('contacts', 'Supplier')
    LegacyPerson = apps.get_model('contacts', 'Person')
    LegacyContactPersonAssoc = apps.get_model('contacts', 'ContactPersonAssociation')
    LegacyPostalAddr = apps.get_model('contacts', 'PostalAddressForContact')
    LegacyEmailAddr = apps.get_model('contacts', 'EmailAddressForContact')
    LegacyPhoneAddr = apps.get_model('contacts', 'PhoneAddressForContact')
    LegacyCustomerGroup = apps.get_model('contacts', 'CustomerGroup')

    Party = apps.get_model('contacts', 'Party')
    Organization = apps.get_model('contacts', 'Organization')
    PartyContact = apps.get_model('contacts', 'PartyContact')
    PartyRole = apps.get_model('contacts', 'PartyRole')
    OrganizationMembership = apps.get_model('contacts', 'OrganizationMembership')
    Address = apps.get_model('contacts', 'Address')
    AddressAssignment = apps.get_model('contacts', 'AddressAssignment')
    PhoneNumber = apps.get_model('contacts', 'PhoneNumber')
    PhoneAssignment = apps.get_model('contacts', 'PhoneAssignment')
    PartyEmail = apps.get_model('contacts', 'PartyEmail')
    EmailAssignment = apps.get_model('contacts', 'EmailAssignment')
    PartyGroup = apps.get_model('contacts', 'PartyGroup')
    PartyGroupMembership = apps.get_model('contacts', 'PartyGroupMembership')

    contact_id_to_party_id = {}
    person_id_to_party_id = {}
    group_id_to_new_group_id = {}
    email_dedup = {}
    phone_dedup = {}
    address_dedup = {}

    # 1. Legacy Contact rows (org-like) -> Party + Organization. Django's MTI
    #    save creates both the parent and child rows atomically; creating the
    #    Party separately would cause a secondary UPDATE that blanks the
    #    parent's auto_now_add fields.
    for legacy_c in LegacyContact.objects.all():
        org = Organization.objects.create(
            display_name=legacy_c.name or f'Party {legacy_c.id}',
            legal_name=legacy_c.name,
        )
        contact_id_to_party_id[legacy_c.id] = org.pk

    # 2. Customer -> PartyRole(customer).
    for cust in LegacyCustomer.objects.all():
        party_id = contact_id_to_party_id.get(cust.pk)
        if not party_id:
            continue
        PartyRole.objects.create(
            party_id=party_id, role_type='customer',
            is_primary=True, valid_from=EPOCH,
        )

    # 3. Supplier -> PartyRole(supplier).
    for sup in LegacySupplier.objects.all():
        party_id = contact_id_to_party_id.get(sup.pk)
        if not party_id:
            continue
        PartyRole.objects.create(
            party_id=party_id, role_type='supplier',
            is_primary=True, valid_from=EPOCH,
        )

    # 4. Legacy Person rows -> Party + PartyContact. Promote Person.email /
    #    Person.phone into standalone + assignment rows.
    for p in LegacyPerson.objects.all():
        display = ' '.join(x for x in [p.pre_name, p.name] if x) or f'Person {p.id}'
        contact = PartyContact.objects.create(
            display_name=display,
            prefix=p.prefix,
            given_name=p.pre_name,
            family_name=p.name,
        )
        person_id_to_party_id[p.id] = contact.pk
        party = contact  # alias for clarity in the blocks below

        if p.email:
            email_id = email_dedup.get(p.email)
            if email_id is None:
                email_id = PartyEmail.objects.create(email=p.email).id
                email_dedup[p.email] = email_id
            EmailAssignment.objects.create(
                party_id=party.id, email_id=email_id,
                purpose='primary', is_primary=True, valid_from=EPOCH,
            )

        if p.phone:
            phone_id = phone_dedup.get(p.phone)
            if phone_id is None:
                phone_id = PhoneNumber.objects.create(phone_e164=p.phone).id
                phone_dedup[p.phone] = phone_id
            PhoneAssignment.objects.create(
                party_id=party.id, phone_id=phone_id,
                purpose='primary', is_primary=True, valid_from=EPOCH,
            )

    # 5. ContactPersonAssociation -> OrganizationMembership.
    for assoc in LegacyContactPersonAssoc.objects.all():
        if not assoc.contact_id or not assoc.person_id:
            continue
        contact_party_id = person_id_to_party_id.get(assoc.person_id)
        org_party_id = contact_id_to_party_id.get(assoc.contact_id)
        if not contact_party_id or not org_party_id:
            continue
        try:
            title = assoc.person.role
        except Exception:  # noqa: BLE001 — historical model is defensive here
            title = None
        OrganizationMembership.objects.create(
            contact_id=contact_party_id,
            organization_id=org_party_id,
            title=title,
            is_primary=False,
            valid_from=EPOCH,
        )

    # 6. PostalAddressForContact -> Address (dedup) + AddressAssignment.
    for pa in LegacyPostalAddr.objects.all():
        key = _addr_key(pa)
        addr_id = address_dedup.get(key)
        if addr_id is None:
            addr_id = Address.objects.create(
                address_line_1=pa.address_line_1,
                address_line_2=pa.address_line_2,
                address_line_3=pa.address_line_3,
                address_line_4=pa.address_line_4,
                zip_code=str(pa.zip_code) if pa.zip_code is not None else None,
                town=pa.town,
                state=pa.state,
                country=pa.country,
                subdivision_code=pa.subdivision_code,
            ).id
            address_dedup[key] = addr_id
        party_id = contact_id_to_party_id.get(pa.person_id)
        if not party_id:
            continue
        AddressAssignment.objects.create(
            party_id=party_id, address_id=addr_id,
            purpose=_map_purpose(pa.purpose),
            is_primary=False, valid_from=EPOCH,
        )

    # 7. EmailAddressForContact -> PartyEmail (dedup) + EmailAssignment.
    for ea in LegacyEmailAddr.objects.all():
        if not ea.email:
            continue
        email_id = email_dedup.get(ea.email)
        if email_id is None:
            email_id = PartyEmail.objects.create(email=ea.email).id
            email_dedup[ea.email] = email_id
        party_id = contact_id_to_party_id.get(ea.person_id)
        if not party_id:
            continue
        EmailAssignment.objects.create(
            party_id=party_id, email_id=email_id,
            purpose=_map_purpose(ea.purpose),
            is_primary=False, valid_from=EPOCH,
        )

    # 8. PhoneAddressForContact -> PhoneNumber (dedup) + PhoneAssignment.
    for ph in LegacyPhoneAddr.objects.all():
        if not ph.phone:
            continue
        phone_id = phone_dedup.get(ph.phone)
        if phone_id is None:
            phone_id = PhoneNumber.objects.create(phone_e164=ph.phone).id
            phone_dedup[ph.phone] = phone_id
        party_id = contact_id_to_party_id.get(ph.person_id)
        if not party_id:
            continue
        PhoneAssignment.objects.create(
            party_id=party_id, phone_id=phone_id,
            purpose=_map_purpose(ph.purpose),
            is_primary=False, valid_from=EPOCH,
        )

    # 9. CustomerGroup -> PartyGroup(role_type_scope='customer').
    for cg in LegacyCustomerGroup.objects.all():
        pg = PartyGroup.objects.create(name=cg.name, role_type_scope='customer')
        group_id_to_new_group_id[cg.id] = pg.id

    # 10. Customer.is_member_of (M2M) -> PartyGroupMembership.
    for cust in LegacyCustomer.objects.all():
        party_id = contact_id_to_party_id.get(cust.pk)
        if not party_id:
            continue
        for cg in cust.is_member_of.all():
            pg_id = group_id_to_new_group_id.get(cg.id)
            if not pg_id:
                continue
            PartyGroupMembership.objects.create(party_id=party_id, party_group_id=pg_id)

    # Invariants (AssertionError rolls back the whole migration).
    legacy_contact_count = LegacyContact.objects.count()
    legacy_person_count = LegacyPerson.objects.count()
    assert Party.objects.count() == legacy_contact_count + legacy_person_count, (
        f"Party count: got {Party.objects.count()}, "
        f"expected {legacy_contact_count + legacy_person_count}"
    )
    assert Organization.objects.count() == legacy_contact_count, (
        f"Organization count: got {Organization.objects.count()}, "
        f"expected {legacy_contact_count}"
    )
    expected_customer_roles = LegacyCustomer.objects.count()
    assert PartyRole.objects.filter(role_type='customer').count() == expected_customer_roles, (
        "customer-role count mismatch"
    )
    expected_supplier_roles = LegacySupplier.objects.count()
    assert PartyRole.objects.filter(role_type='supplier').count() == expected_supplier_roles, (
        "supplier-role count mismatch"
    )


def reverse(apps, schema_editor):
    """Truncate the new tables. Legacy tables are never touched."""
    for model_name in (
        'PartyGroupMembership',
        'PartyGroup',
        'EmailAssignment',
        'PartyEmail',
        'PhoneAssignment',
        'PhoneNumber',
        'AddressAssignment',
        'Address',
        'OrganizationRelationship',
        'OrganizationMembership',
        'PartyRole',
        'PartyIdentification',
        'PartyContact',
        'Organization',
        'Party',
    ):
        apps.get_model('contacts', model_name).objects.all().delete()


def row_count_report(apps):
    """Compute a {label: (legacy_count, new_count, delta)} report.

    Shared between the `contacts_backfill_dryrun` and `contacts_backfill_reconcile`
    management commands. Computing `new_count` on the pre-migration state gives
    dryrun its expected-vs-zero view; computing it after the migration gives
    reconcile its expected-vs-actual view.
    """
    LegacyContact = apps.get_model('contacts', 'Contact')
    LegacyCustomer = apps.get_model('contacts', 'Customer')
    LegacySupplier = apps.get_model('contacts', 'Supplier')
    LegacyPerson = apps.get_model('contacts', 'Person')
    LegacyContactPersonAssoc = apps.get_model('contacts', 'ContactPersonAssociation')
    LegacyPostalAddr = apps.get_model('contacts', 'PostalAddressForContact')
    LegacyEmailAddr = apps.get_model('contacts', 'EmailAddressForContact')
    LegacyPhoneAddr = apps.get_model('contacts', 'PhoneAddressForContact')
    LegacyCustomerGroup = apps.get_model('contacts', 'CustomerGroup')

    Party = apps.get_model('contacts', 'Party')
    Organization = apps.get_model('contacts', 'Organization')
    PartyContact = apps.get_model('contacts', 'PartyContact')
    PartyRole = apps.get_model('contacts', 'PartyRole')
    OrganizationMembership = apps.get_model('contacts', 'OrganizationMembership')
    PartyGroup = apps.get_model('contacts', 'PartyGroup')

    contact_n = LegacyContact.objects.count()
    person_n = LegacyPerson.objects.count()
    customer_n = LegacyCustomer.objects.count()
    supplier_n = LegacySupplier.objects.count()

    return [
        # label, expected_new_count, actual_new_count
        ('Party',                    contact_n + person_n, Party.objects.count()),
        ('Organization',             contact_n,            Organization.objects.count()),
        ('PartyContact',             person_n,             PartyContact.objects.count()),
        ('PartyRole(customer)',      customer_n,           PartyRole.objects.filter(role_type='customer').count()),
        ('PartyRole(supplier)',      supplier_n,           PartyRole.objects.filter(role_type='supplier').count()),
        ('OrganizationMembership',   LegacyContactPersonAssoc.objects.count(), OrganizationMembership.objects.count()),
        ('AddressAssignment (from postal)', LegacyPostalAddr.objects.count(),  apps.get_model('contacts', 'AddressAssignment').objects.count()),
        ('EmailAssignment (from email-for-contact + person.email)',
            LegacyEmailAddr.objects.count() + LegacyPerson.objects.exclude(email='').count(),
            apps.get_model('contacts', 'EmailAssignment').objects.count()),
        ('PhoneAssignment (from phone-for-contact + person.phone)',
            LegacyPhoneAddr.objects.count() + LegacyPerson.objects.exclude(phone='').count(),
            apps.get_model('contacts', 'PhoneAssignment').objects.count()),
        ('PartyGroup',               LegacyCustomerGroup.objects.count(), PartyGroup.objects.count()),
    ]
