"""Backfill Party.default_billing_cycle from legacy Customer rows.

Moved-in-G3 data population: `default_customer_billing_cycle` used to
live on the legacy Customer model. With Customer being dropped, its
billing-cycle FK moves onto Party (0007 added the column; this
migration populates it).

Idempotent — only sets the value where it is currently NULL. Safe to
re-run; safe on a fresh DB (nothing to do).
"""
from django.db import migrations


def forwards(apps, schema_editor):
    LegacyCustomer = apps.get_model('contacts', 'Customer')
    Party = apps.get_model('contacts', 'Party')

    # Reuse the same pk-ordered zip the FK-rewire migrations use to map
    # legacy_contact_id -> party_id. Inline the mapping here to avoid
    # importing from koalixcrm.contacts.backfill (which imports apps-
    # registry at module load).
    LegacyContact = apps.get_model('contacts', 'Contact')
    Organization = apps.get_model('contacts', 'Organization')
    legacy_ids = list(
        LegacyContact.objects.order_by('pk').values_list('pk', flat=True)
    )
    party_ids = list(
        Organization.objects.order_by('pk').values_list('pk', flat=True)
    )
    if len(legacy_ids) != len(party_ids):
        # Should be impossible at this point — 0006_verify_ready_for_cutover
        # already asserted the counts match. Defensive bail-out.
        return
    mapping = dict(zip(legacy_ids, party_ids))

    for cust in LegacyCustomer.objects.all():
        party_id = mapping.get(cust.pk)
        if party_id is None:
            continue
        cycle_id = cust.default_customer_billing_cycle_id
        if cycle_id is None:
            continue
        Party.objects.filter(pk=party_id, default_billing_cycle__isnull=True).update(
            default_billing_cycle_id=cycle_id,
        )


def noop(apps, schema_editor):
    # Reverse is a no-op — dropping the column (in a future migration) is
    # the proper way to undo this; setting every row back to NULL would
    # be destructive.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0007_party_default_billing_cycle'),
    ]

    operations = [
        migrations.RunPython(forwards, noop),
    ]
