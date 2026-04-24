"""Add Party-pattern FKs to Contract and CommercialDocument (issue #394).

Adds three nullable ForeignKeys (Contract.buyer_party, Contract.supplier_party,
CommercialDocument.party) and populates them from the legacy FKs via
`koalixcrm.contracts.party_fk_rewire`. Legacy FKs remain in place as
nullable shadows until #395.

"""
import django.db.models.deletion
from django.db import migrations, models

from koalixcrm.contracts.party_fk_rewire import populate_party_fks, clear_party_fks


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0005_backfill_party'),
        ('contract_object_management', '0007_ubl_document_meta'),
    ]

    operations = [
        migrations.AddField(
            model_name='commercialdocument',
            name='party',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='commercial_documents',
                to='contacts.party',
                verbose_name='Party',
            ),
        ),
        migrations.AddField(
            model_name='contract',
            name='buyer_party',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='contracts_as_buyer',
                to='contacts.party',
                verbose_name='Buyer (Party)',
            ),
        ),
        migrations.AddField(
            model_name='contract',
            name='supplier_party',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='contracts_as_supplier',
                to='contacts.party',
                verbose_name='Supplier (Party)',
            ),
        ),
        migrations.RunPython(populate_party_fks, clear_party_fks),
    ]
