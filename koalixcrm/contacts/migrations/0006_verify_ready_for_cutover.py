"""Pre-cutover verification gate (issue #395 G2).

Non-destructive. Runs every invariant defined in
`koalixcrm.contacts.backfill_verify` and raises
`BackfillVerificationError` if any check fails — which aborts `migrate`
before any destructive operation runs.

This migration is the documented checkpoint: once it is recorded as
applied in `django_migrations`, the destructive migrations that follow
(drop legacy FK columns, drop legacy models) can run safely. If it
fails, `migrate` halts before those migrations are ever reached.

Reverse is a no-op — there's nothing to undo, and re-running `migrate`
will re-execute the verify automatically.
"""
from django.db import migrations


def verify(apps, schema_editor):
    from koalixcrm.contacts.backfill_verify import verify_ready_for_cutover
    verify_ready_for_cutover(apps, raise_on_failure=True)


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0005_backfill_party'),
        ('contract_object_management', '0008_party_fks'),
        ('products', '0002_party_group_fks'),
    ]

    operations = [
        migrations.RunPython(verify, noop),
    ]
