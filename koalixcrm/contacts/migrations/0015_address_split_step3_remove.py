# -*- coding: utf-8 -*-
"""Step 3 of the Address field migration: remove legacy fields."""
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0014_address_split_step2_data'),
    ]

    operations = [
        migrations.RemoveField(model_name='address', name='address_line_1'),
        migrations.RemoveField(model_name='address', name='address_line_2'),
        migrations.RemoveField(model_name='address', name='address_line_3'),
        migrations.RemoveField(model_name='address', name='address_line_4'),
    ]
