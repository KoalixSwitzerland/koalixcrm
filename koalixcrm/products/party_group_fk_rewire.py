# -*- coding: utf-8 -*-
"""Populate products.Price.party_group and products.CustomerGroupTransform
`from_party_group` / `to_party_group` from the legacy CustomerGroup FKs.

Called from migration 0002_party_group_fks (via RunPython) and from tests.
Separate module because migration filenames start with a digit.

"""
from __future__ import annotations

from typing import TYPE_CHECKING

from koalixcrm.contacts.backfill import (
    build_legacy_customer_group_to_party_group_mapping,
)

if TYPE_CHECKING:
    from django.apps.registry import Apps
    from django.db.backends.base.schema import BaseDatabaseSchemaEditor


def populate_party_group_fks(apps: Apps, schema_editor: BaseDatabaseSchemaEditor | None) -> None:
    Price = apps.get_model('products', 'Price')
    CustomerGroupTransform = apps.get_model('products', 'CustomerGroupTransform')

    mapping = build_legacy_customer_group_to_party_group_mapping(apps)
    if not mapping:
        return

    for price in Price.objects.filter(
        party_group__isnull=True, customer_group__isnull=False,
    ):
        new_id = mapping.get(price.customer_group_id)
        if new_id:
            price.party_group_id = new_id
            price.save(update_fields=['party_group'])

    for t in CustomerGroupTransform.objects.filter(
        from_party_group__isnull=True, from_customer_group__isnull=False,
    ):
        new_id = mapping.get(t.from_customer_group_id)
        if new_id:
            t.from_party_group_id = new_id
            t.save(update_fields=['from_party_group'])

    for t in CustomerGroupTransform.objects.filter(
        to_party_group__isnull=True, to_customer_group__isnull=False,
    ):
        new_id = mapping.get(t.to_customer_group_id)
        if new_id:
            t.to_party_group_id = new_id
            t.save(update_fields=['to_party_group'])


def clear_party_group_fks(apps: Apps, schema_editor: BaseDatabaseSchemaEditor | None) -> None:
    Price = apps.get_model('products', 'Price')
    CustomerGroupTransform = apps.get_model('products', 'CustomerGroupTransform')
    Price.objects.update(party_group=None)
    CustomerGroupTransform.objects.update(from_party_group=None, to_party_group=None)
