# -*- coding: utf-8 -*-
"""Pre-cutover verification for the Party data migration (issue #395 G2).

This is the last safety gate before v2.0.0 drops the legacy Contact /
Customer / Supplier / Person / CustomerGroup tables. Every check here
is re-runnable and idempotent — on a healthy DB the verifier is a
~100-ms read-only sweep; on an unhealthy DB it prints a list of
actionable remediation hints and refuses to proceed.

The same entry point (`verify_ready_for_cutover`) is called from
three places:

  1. Django migration `contacts.0006_verify_ready_for_cutover` — gates
     the destructive migrations that follow.
  2. Management command `manage.py contacts_backfill_reconcile` —
     operator-facing dry-run, no raising, full report to stdout.
  3. Integration tests — programmatic call with `raise_on_failure=True`.

See `docs/migration-v1.14.0-to-v2.0.0.md` for what to do when a check
fails.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.apps.registry import Apps


@dataclass
class Check:
    name: str
    passed: bool
    legacy_count: int
    new_count: int
    hint: str = ''  # only populated when passed is False

    @property
    def delta(self) -> int:
        return self.new_count - self.legacy_count


class BackfillVerificationError(RuntimeError):
    """Raised when the pre-cutover verifier finds an invariant violation.

    The string representation lists every failed check with the
    diagnostic hint. Catch this at the operator boundary, not inside
    the migration — the migration should abort.
    """

    def __init__(self, failed_checks: list[Check]):
        self.failed_checks = failed_checks
        super().__init__(self._format())

    def _format(self) -> str:
        lines = [
            "Pre-cutover verification failed — refusing to drop legacy tables.",
            "",
            "Failed invariants:",
        ]
        for c in self.failed_checks:
            lines.append(
                f"  ✗ {c.name}: expected {c.legacy_count}, got {c.new_count} "
                f"(delta {c.delta:+d})"
            )
            if c.hint:
                lines.append(f"      hint: {c.hint}")
        lines.append("")
        lines.append(
            "Full remediation guide: "
            "docs/migration-v1.14.0-to-v2.0.0.md#upgrading-contacts-data-to-the-party-model"
        )
        return "\n".join(lines)


def verify_ready_for_cutover(apps: Apps, *, raise_on_failure: bool = True) -> list[Check]:
    """Run every pre-cutover invariant. Return the full check list.

    When `raise_on_failure=True` and one or more checks fail, raise
    :class:`BackfillVerificationError` with the full list of failures.
    Callers that want a non-raising report (e.g. the reconcile
    management command) pass `raise_on_failure=False` and inspect the
    returned list.
    """
    checks = _run_checks(apps)
    failed = [c for c in checks if not c.passed]
    if failed and raise_on_failure:
        raise BackfillVerificationError(failed)
    return checks


def _run_checks(apps: Apps) -> list[Check]:
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
    AddressAssignment = apps.get_model('contacts', 'AddressAssignment')
    EmailAssignment = apps.get_model('contacts', 'EmailAssignment')
    PhoneAssignment = apps.get_model('contacts', 'PhoneAssignment')
    PartyGroup = apps.get_model('contacts', 'PartyGroup')

    Contract = apps.get_model('contract_object_management', 'Contract')
    CommercialDocument = apps.get_model('contract_object_management', 'CommercialDocument')
    Price = apps.get_model('products', 'Price')
    CustomerGroupTransform = apps.get_model('products', 'CustomerGroupTransform')

    contact_n = LegacyContact.objects.count()
    person_n = LegacyPerson.objects.count()
    customer_n = LegacyCustomer.objects.count()
    supplier_n = LegacySupplier.objects.count()

    checks: list[Check] = []

    def add(name: str, legacy_count: int, new_count: int, *, hint: str = '') -> None:
        checks.append(Check(
            name=name,
            passed=(legacy_count == new_count),
            legacy_count=legacy_count,
            new_count=new_count,
            hint=hint if legacy_count != new_count else '',
        ))

    # --- Count invariants from the backfill (PR #393) ---
    add(
        'Party.count == legacy Contact.count + legacy Person.count',
        contact_n + person_n, Party.objects.count(),
        hint=_HINT_BACKFILL,
    )
    add(
        'Organization.count == legacy Contact.count',
        contact_n, Organization.objects.count(),
        hint=_HINT_BACKFILL,
    )
    add(
        'PartyContact.count == legacy Person.count',
        person_n, PartyContact.objects.count(),
        hint=_HINT_BACKFILL,
    )
    add(
        'PartyRole(customer).count == legacy Customer.count',
        customer_n, PartyRole.objects.filter(role_type='customer').count(),
        hint=_HINT_BACKFILL,
    )
    add(
        'PartyRole(supplier).count == legacy Supplier.count',
        supplier_n, PartyRole.objects.filter(role_type='supplier').count(),
        hint=_HINT_BACKFILL,
    )
    add(
        'OrganizationMembership.count == legacy ContactPersonAssociation.count',
        LegacyContactPersonAssoc.objects.count(), OrganizationMembership.objects.count(),
        hint=_HINT_BACKFILL,
    )
    add(
        'AddressAssignment.count >= legacy PostalAddressForContact.count',
        LegacyPostalAddr.objects.count(), AddressAssignment.objects.count(),
        hint=_HINT_BACKFILL,
    )
    add(
        'EmailAssignment.count >= legacy EmailAddressForContact.count + Person.email-having',
        LegacyEmailAddr.objects.count() + LegacyPerson.objects.exclude(email='').count(),
        EmailAssignment.objects.count(),
        hint=_HINT_BACKFILL,
    )
    add(
        'PhoneAssignment.count >= legacy PhoneAddressForContact.count + Person.phone-having',
        LegacyPhoneAddr.objects.count() + LegacyPerson.objects.exclude(phone='').count(),
        PhoneAssignment.objects.count(),
        hint=_HINT_BACKFILL,
    )
    add(
        'PartyGroup.count == legacy CustomerGroup.count',
        LegacyCustomerGroup.objects.count(), PartyGroup.objects.count(),
        hint=_HINT_BACKFILL,
    )

    # --- FK-rewire invariants (PR #394 Phase A / B) ---
    # "Every document with a legacy FK set has its new FK set too." The count
    # we compare against is the population of the legacy field; the "new"
    # count is how many of those have the new FK populated.
    contracts_with_customer = Contract.objects.filter(default_customer__isnull=False).count()
    contracts_with_customer_party = Contract.objects.filter(
        default_customer__isnull=False, buyer_party__isnull=False,
    ).count()
    add(
        'Contract: buyer_party set for every Contract with default_customer',
        contracts_with_customer, contracts_with_customer_party,
        hint=_HINT_FK_REWIRE.format(app='contracts', field='buyer_party'),
    )

    contracts_with_supplier = Contract.objects.filter(default_supplier__isnull=False).count()
    contracts_with_supplier_party = Contract.objects.filter(
        default_supplier__isnull=False, supplier_party__isnull=False,
    ).count()
    add(
        'Contract: supplier_party set for every Contract with default_supplier',
        contracts_with_supplier, contracts_with_supplier_party,
        hint=_HINT_FK_REWIRE.format(app='contracts', field='supplier_party'),
    )

    docs_with_customer = CommercialDocument.objects.filter(customer__isnull=False).count()
    docs_with_party = CommercialDocument.objects.filter(
        customer__isnull=False, party__isnull=False,
    ).count()
    add(
        'CommercialDocument: party set for every document with customer',
        docs_with_customer, docs_with_party,
        hint=_HINT_FK_REWIRE.format(app='contracts', field='party'),
    )

    prices_with_group = Price.objects.filter(customer_group__isnull=False).count()
    prices_with_party_group = Price.objects.filter(
        customer_group__isnull=False, party_group__isnull=False,
    ).count()
    add(
        'Price: party_group set for every Price with customer_group',
        prices_with_group, prices_with_party_group,
        hint=_HINT_FK_REWIRE.format(app='products', field='party_group'),
    )

    transforms_total = CustomerGroupTransform.objects.count()
    transforms_complete = CustomerGroupTransform.objects.filter(
        from_party_group__isnull=False, to_party_group__isnull=False,
    ).count()
    add(
        'CustomerGroupTransform: both from_/to_party_group set on every row',
        transforms_total, transforms_complete,
        hint=_HINT_FK_REWIRE.format(app='products', field='from_/to_party_group'),
    )

    return checks


# --- Hint bodies (kept as module constants to keep the check list legible) ---

_HINT_BACKFILL = (
    "Row count drift between legacy and new tables. Usually means the "
    "legacy data has orphans or duplicates that the backfill couldn't "
    "resolve. Fix in v1.14.0 first (see docs — 'upgrading contacts data "
    "to the Party model'), then retry the v2.0.0 upgrade on a DB copy."
)

_HINT_FK_REWIRE = (
    "Some {app}.{field} rows have the legacy FK populated but the new "
    "FK is null. Re-run the FK-rewire migration for that app; if it "
    "still fails, the legacy FK points at a row that was NOT migrated "
    "into the new Party tables — fix the source row in v1.14.0 first."
)
