# -*- coding: utf-8 -*-
"""Rename CommercialDocument.external_reference -> party_reference and
add ext_business_appl_references JSONField.
"""
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contract_object_management', '0014_commercial_document_address_assignments'),
    ]

    operations = [
        migrations.RenameField(
            model_name='commercialdocument',
            old_name='external_reference',
            new_name='party_reference',
        ),
        migrations.AlterField(
            model_name='commercialdocument',
            name='party_reference',
            field=models.CharField(blank=True, max_length=100, verbose_name='Party Reference'),
        ),
        migrations.AddField(
            model_name='commercialdocument',
            name='ext_business_appl_references',
            field=models.JSONField(blank=True, default=dict, verbose_name='External Business Application References'),
        ),
    ]
