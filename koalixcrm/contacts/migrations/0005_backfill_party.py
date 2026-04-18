"""Data migration: legacy contacts -> Party data model.

Implements §PR #2 of PLAN_contact_party_data_model.md. Forward / reverse
logic lives in `koalixcrm.contacts.backfill` so it's callable from tests
and management commands — migration filenames start with a digit and are
not valid Python identifiers for direct import.

See ADR 0001 in KoalixSwitzerland/koalixcrm_system and issue #393.
"""
from django.db import migrations

from koalixcrm.contacts.backfill import forwards, reverse


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0004_party_data_model'),
    ]

    operations = [
        migrations.RunPython(forwards, reverse),
    ]
