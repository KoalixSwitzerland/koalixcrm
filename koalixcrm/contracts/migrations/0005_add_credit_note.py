# -*- coding: utf-8 -*-
"""Add CreditNote model as a sibling of Invoice under CommercialDocument."""

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("contract_object_management", "0004_rename_sales_document_to_commercial_document"),
    ]

    operations = [
        migrations.CreateModel(
            name="CreditNote",
            fields=[
                (
                    "commercialdocument_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="contract_object_management.commercialdocument",
                    ),
                ),
                (
                    "corrects_invoice",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="contract_object_management.invoice",
                        verbose_name="Corrects Invoice",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("C", "Credit note created"),
                            ("S", "Credit note sent"),
                            ("B", "Booked"),
                            ("D", "Deleted"),
                        ],
                        max_length=1,
                    ),
                ),
                (
                    "issue_date",
                    models.DateField(verbose_name="Issue Date"),
                ),
                (
                    "reason",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=200,
                        verbose_name="Reason",
                    ),
                ),
            ],
            options={
                "db_table": "crm_creditnote",
                "verbose_name": "Credit Note",
                "verbose_name_plural": "Credit Notes",
            },
            bases=("contract_object_management.commercialdocument",),
        ),
    ]
