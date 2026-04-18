"""Tighten CustomerGroupTransform.from_/to_party_group to NOT NULL
(issue #395 G2).

Precondition: contacts.0006_verify_ready_for_cutover has asserted that
every row has both Party-pattern FKs set. Safe without a default.

Price.party_group stays nullable — the legacy customer_group was optional
and the new semantics preserve that.
"""
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0006_verify_ready_for_cutover'),
        ('products', '0002_party_group_fks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customergrouptransform',
            name='from_party_group',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='transforms_from',
                to='contacts.partygroup',
                verbose_name='From Party Group',
            ),
        ),
        migrations.AlterField(
            model_name='customergrouptransform',
            name='to_party_group',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='transforms_to',
                to='contacts.partygroup',
                verbose_name='To Party Group',
            ),
        ),
    ]
