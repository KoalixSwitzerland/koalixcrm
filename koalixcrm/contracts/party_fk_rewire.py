# -*- coding: utf-8 -*-
"""Populate Contract / CommercialDocument Party FKs from the legacy FKs.

Called from migration `0008_party_fks` (via RunPython) and from tests. Kept
in a standalone module because migration filenames start with a digit and
aren't importable as Python modules.

"""
from koalixcrm.contacts.backfill import build_legacy_contact_to_party_mapping


def populate_party_fks(apps, schema_editor):
    Contract = apps.get_model('contract_object_management', 'Contract')
    CommercialDocument = apps.get_model('contract_object_management', 'CommercialDocument')

    mapping = build_legacy_contact_to_party_mapping(apps)
    if not mapping:
        return

    for contract in Contract.objects.filter(
        buyer_party__isnull=True, default_customer__isnull=False,
    ):
        party_id = mapping.get(contract.default_customer_id)
        if party_id:
            contract.buyer_party_id = party_id
            contract.save(update_fields=['buyer_party'])

    for contract in Contract.objects.filter(
        supplier_party__isnull=True, default_supplier__isnull=False,
    ):
        party_id = mapping.get(contract.default_supplier_id)
        if party_id:
            contract.supplier_party_id = party_id
            contract.save(update_fields=['supplier_party'])

    for doc in CommercialDocument.objects.filter(
        party__isnull=True, customer__isnull=False,
    ):
        party_id = mapping.get(doc.customer_id)
        if party_id:
            doc.party_id = party_id
            doc.save(update_fields=['party'])


def clear_party_fks(apps, schema_editor):
    Contract = apps.get_model('contract_object_management', 'Contract')
    CommercialDocument = apps.get_model('contract_object_management', 'CommercialDocument')
    Contract.objects.update(buyer_party=None, supplier_party=None)
    CommercialDocument.objects.update(party=None)
