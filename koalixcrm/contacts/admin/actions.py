# -*- coding: utf-8 -*-
"""Bulk admin actions for reclassifying parties between Organization and
natural-person Contact (PartyContact).

Useful for two cases:

1. Post-migration cleanup: the v1.14.0 → v2.0.0 backfill couldn't tell
   a company-like Contact row apart from a person-like one (there was
   no flag in the legacy schema). Everything landed as Organization;
   this action moves misclassified rows to Contact in bulk.

2. Ongoing data hygiene: users occasionally register a private person
   as an Organization (or the other way around). Same action covers
   the fix without having to delete + recreate + relink documents.

The conversion preserves the underlying Party row — the Party's ID, its
attached PartyRole rows, AddressAssignment / PhoneAssignment /
EmailAssignment, PartyIdentification, and every document FK pointing
at the Party continue to work unchanged. Only the MTI-child row in
crm_organization / crm_partycontact is swapped. OrganizationMembership
and OrganizationRelationship rows involving the converted Organization
are deleted (they become meaningless for a natural person).
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib import admin, messages
from django.db import connection, models, transaction
from django.utils.translation import gettext_lazy as _

from koalixcrm.contacts.models.natural_person import PartyContact
from koalixcrm.contacts.models.organization import Organization
from koalixcrm.contacts.models.organization_membership import OrganizationMembership
from koalixcrm.contacts.models.organization_relationship import OrganizationRelationship

if TYPE_CHECKING:
    from django.contrib.admin import ModelAdmin
    from django.db.models import QuerySet
    from django.http import HttpRequest


def _split_display_name(display_name: str | None) -> tuple[str, str]:
    """Best-effort split of 'Jane Doe' → ('Jane', 'Doe').

    Falls back to empty given_name + full string as family_name when the
    display_name has no space. The admin can refine manually afterwards —
    the point of the bulk action is to flip the MTI subclass, not to
    guess names perfectly.
    """
    if not display_name:
        return '', ''
    parts = display_name.strip().split(None, 1)
    if len(parts) == 1:
        return '', parts[0]
    return parts[0], parts[1]


@admin.action(description=_(
    "Convert selected Organizations to Contacts (natural persons)"
))
def convert_organizations_to_contacts(
    modeladmin: ModelAdmin, request: HttpRequest, queryset: QuerySet[Organization]
) -> None:
    converted = 0
    skipped_existing = 0
    removed_memberships = 0
    removed_relationships = 0

    for org in queryset.only('pk', 'display_name'):
        party_id = org.pk
        if PartyContact.objects.filter(pk=party_id).exists():
            skipped_existing += 1
            continue
        given, family = _split_display_name(org.display_name)
        with transaction.atomic():
            m_deleted, _details = OrganizationMembership.objects.filter(
                organization_id=party_id,
            ).delete()
            r_deleted, _details = OrganizationRelationship.objects.filter(
                models.Q(parent_id=party_id) | models.Q(child_id=party_id),
            ).delete()
            with connection.cursor() as cursor:
                # Delete only the MTI-child row. Using the ORM would cascade
                # onto the parent Party (and take every PartyRole / address /
                # phone / email with it) — exactly what we're trying to avoid.
                cursor.execute(
                    'DELETE FROM crm_organization WHERE party_ptr_id = %s',
                    [party_id],
                )
                cursor.execute(
                    'INSERT INTO crm_partycontact '
                    '(party_ptr_id, given_name, family_name) '
                    'VALUES (%s, %s, %s)',
                    [party_id, given, family],
                )
            converted += 1
            removed_memberships += m_deleted
            removed_relationships += r_deleted

    modeladmin.message_user(
        request,
        _(
            "Converted {converted} organization(s) to contacts. "
            "Removed {memberships} employee membership(s) and "
            "{relationships} organization relationship(s). "
            "Skipped {skipped} organization(s) that already had a Contact row."
        ).format(
            converted=converted,
            memberships=removed_memberships,
            relationships=removed_relationships,
            skipped=skipped_existing,
        ),
        messages.SUCCESS if converted else messages.WARNING,
    )


@admin.action(description=_(
    "Convert selected Contacts to Organizations"
))
def convert_contacts_to_organizations(
    modeladmin: ModelAdmin, request: HttpRequest, queryset: QuerySet[PartyContact]
) -> None:
    converted = 0
    skipped_existing = 0

    for contact in queryset.only('pk', 'display_name', 'given_name', 'family_name'):
        party_id = contact.pk
        if Organization.objects.filter(pk=party_id).exists():
            skipped_existing += 1
            continue
        # Recombine the name into a legal_name so the Organization edit page
        # shows a populated legal_name field. display_name on the parent
        # Party is untouched.
        legal_name = ' '.join(
            p for p in (contact.given_name, contact.family_name) if p
        ) or contact.display_name
        with transaction.atomic():
            with connection.cursor() as cursor:
                cursor.execute(
                    'DELETE FROM crm_partycontact WHERE party_ptr_id = %s',
                    [party_id],
                )
                cursor.execute(
                    'INSERT INTO crm_organization '
                    '(party_ptr_id, legal_name) '
                    'VALUES (%s, %s)',
                    [party_id, legal_name],
                )
            converted += 1

    modeladmin.message_user(
        request,
        _(
            "Converted {converted} contact(s) to organizations. "
            "Skipped {skipped} contact(s) that already had an Organization row."
        ).format(converted=converted, skipped=skipped_existing),
        messages.SUCCESS if converted else messages.WARNING,
    )
