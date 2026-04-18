"""Drop legacy customer/supplier FK columns on documents (issue #395 G3).

Runs after:
  - contacts.0006_verify_ready_for_cutover has confirmed every document's
    new Party FK is populated.
  - contracts.0009_tighten_party_fk has made CommercialDocument.party
    NOT NULL.
  - contacts.0008_backfill_party_billing_cycle has moved the billing-cycle
    data off legacy Customer.

After this migration the contracts app no longer references any legacy
contacts model. contacts.0009_drop_legacy_models (in the contacts app)
then drops the legacy tables themselves.
"""
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contract_object_management', '0009_tighten_party_fk'),
        ('contacts', '0008_backfill_party_billing_cycle'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commercialdocument',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='contract',
            name='default_customer',
        ),
        migrations.RemoveField(
            model_name='contract',
            name='default_supplier',
        ),
        migrations.RemoveField(
            model_name='purchaseorder',
            name='supplier',
        ),
    ]
