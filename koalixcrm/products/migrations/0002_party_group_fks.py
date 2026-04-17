"""Add Party-pattern FKs to products.Price and products.CustomerGroupTransform
(issue #394 Phase B).

Adds three nullable ForeignKeys and populates them from the legacy
`customer_group` FKs via `koalixcrm.products.party_group_fk_rewire`. Legacy
FKs remain in place as shadows until #395.
"""
import django.db.models.deletion
from django.db import migrations, models

from koalixcrm.products.party_group_fk_rewire import (
    populate_party_group_fks, clear_party_group_fks,
)


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0005_backfill_party'),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customergrouptransform',
            name='from_party_group',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='transforms_from',
                to='contacts.partygroup',
                verbose_name='From Party Group',
            ),
        ),
        migrations.AddField(
            model_name='customergrouptransform',
            name='to_party_group',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='transforms_to',
                to='contacts.partygroup',
                verbose_name='To Party Group',
            ),
        ),
        migrations.AddField(
            model_name='price',
            name='party_group',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='prices',
                to='contacts.partygroup',
                verbose_name='Party Group',
            ),
        ),
        migrations.RunPython(populate_party_group_fks, clear_party_group_fks),
    ]
