# -*- coding: utf-8 -*-
"""Step 1 of the Address field migration: add new fields."""
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0012_drop_address_bases'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='street',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Street'),
        ),
        migrations.AddField(
            model_name='address',
            name='number',
            field=models.CharField(blank=True, max_length=16, null=True, verbose_name='Number'),
        ),
        migrations.AddField(
            model_name='address',
            name='additional_address_line_1',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Additional address line 1'),
        ),
        migrations.AddField(
            model_name='address',
            name='additional_address_line_2',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Additional address line 2'),
        ),
        migrations.AddField(
            model_name='address',
            name='additional_address_line_3',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Additional address line 3'),
        ),
    ]
