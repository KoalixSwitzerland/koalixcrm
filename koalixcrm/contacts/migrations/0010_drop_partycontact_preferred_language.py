"""Drop PartyContact.preferred_language (duplicate of Party.default_language).

Party already carries a `default_language` field that PartyContact
inherits via MTI. `preferred_language` was added separately on the
PartyContact subclass and ended up showing as two fields in the admin
for natural persons. Consolidated onto Party.default_language.

Before dropping the column: copy any populated preferred_language
values onto Party.default_language where the parent is still NULL,
so we don't lose user data on upgrade.
"""
from django.db import migrations


def copy_preferred_language_up_to_party(apps, schema_editor):
    PartyContact = apps.get_model('contacts', 'PartyContact')
    Party = apps.get_model('contacts', 'Party')
    for contact in PartyContact.objects.exclude(preferred_language__isnull=True):
        if not contact.preferred_language:
            continue
        Party.objects.filter(
            pk=contact.pk, default_language__isnull=True,
        ).update(default_language=contact.preferred_language)


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0009_drop_legacy_models'),
    ]

    operations = [
        migrations.RunPython(copy_preferred_language_up_to_party, noop),
        migrations.RemoveField(
            model_name='partycontact',
            name='preferred_language',
        ),
    ]
