"""Drop legacy customer_group FK columns on products (issue #395 G3).

Runs after contacts.0006_verify_ready_for_cutover has confirmed every
Price.party_group / CustomerGroupTransform.from_/to_party_group is
populated.
"""
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_tighten_party_group_fks'),
        ('contacts', '0006_verify_ready_for_cutover'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customergrouptransform',
            name='from_customer_group',
        ),
        migrations.RemoveField(
            model_name='customergrouptransform',
            name='to_customer_group',
        ),
        migrations.RemoveField(
            model_name='price',
            name='customer_group',
        ),
    ]
