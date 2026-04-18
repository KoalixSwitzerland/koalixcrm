"""Tighten CommercialDocument.party to NOT NULL (issue #395 G2).

Precondition: contacts.0006_verify_ready_for_cutover has asserted that
every CommercialDocument with a legacy `customer` has `party` set. If
that migration applied, there are no null `party` rows; this AlterField
is safe without a default.

Legacy `customer` / `default_customer` / `default_supplier` columns are
untouched here — they are removed in #395 G3 together with the legacy
models themselves. `Contract.buyer_party` and `Contract.supplier_party`
stay nullable to match the legacy `default_customer` / `default_supplier`
semantics (both were optional).
"""
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0006_verify_ready_for_cutover'),
        ('contract_object_management', '0008_party_fks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commercialdocument',
            name='party',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='commercial_documents',
                to='contacts.party',
                verbose_name='Party',
            ),
        ),
    ]
