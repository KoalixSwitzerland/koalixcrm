# -*- coding: utf-8 -*-
"""ADR-0003 (Produkt-Katalog-Backbone) + ADR-0021 (Topologie/Schlüsselung).

Builds out the full backbone on top of the 0007 rename:
  - `Product`: rename `default_unit` -> `base_uom`, `tax` -> `tax_class`
    (canonical ADR-0003 field names); add `lifecycle_status`, `brand`,
    `manufacturer_party` (FK contacts.Party), `country_of_origin`,
    `product_family` (FK, nullable — ADR-0021 Korrektur 1: ProductFamily
    groups Product, not ProductVariant).
  - New models: `ProductFamily`, `ProductVariant` (FK -> Product per
    ADR-0021 Korrektur 2; carries sku/gtin/mpn/weight_kg/dimensions_* per
    the ADR-0021 keying table), `ProductTranslation`, `ProductMedia`.

Plain field renames (not an FK-lift), so no 3-phase pattern is required.
"""
from __future__ import annotations

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_rename_producttype_to_product'),
        ('contacts', '0016_party_ext_business_appl_references_and_more'),
        ('core', '0008_remove_roleinworkspace_crm_riw_group_ws_idx_and_more'),
    ]

    operations = [
        # ── Product: canonical field renames ────────────────────────────
        migrations.RenameField(
            model_name='product',
            old_name='default_unit',
            new_name='base_uom',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='tax',
            new_name='tax_class',
        ),
        migrations.AlterField(
            model_name='product',
            name='base_uom',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to='core.unit',
                verbose_name='Base Unit of Measure',
            ),
        ),
        migrations.AlterField(
            model_name='product',
            name='tax_class',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to='core.tax',
                verbose_name='Tax Class',
            ),
        ),
        # ── Product: new Layer-1 fields ─────────────────────────────────
        migrations.AddField(
            model_name='product',
            name='lifecycle_status',
            field=models.CharField(
                choices=[
                    ('DRAFT', 'Draft'),
                    ('ACTIVE', 'Active'),
                    ('DISCONTINUED', 'Discontinued'),
                    ('ARCHIVED', 'Archived'),
                    ('EXTERNAL_ONLY', 'External Only'),
                ],
                default='DRAFT',
                max_length=32,
                verbose_name='Lifecycle Status',
            ),
        ),
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Brand'),
        ),
        migrations.AddField(
            model_name='product',
            name='manufacturer_party',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='manufactured_products',
                to='contacts.party',
                verbose_name='Manufacturer',
            ),
        ),
        migrations.AddField(
            model_name='product',
            name='country_of_origin',
            field=models.CharField(
                blank=True,
                max_length=2,
                null=True,
                help_text='ISO 3166-1 alpha-2 country code.',
                verbose_name='Country of Origin',
            ),
        ),
        # ── ProductFamily ────────────────────────────────────────────────
        migrations.CreateModel(
            name='ProductFamily',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('last_modification', models.DateTimeField(auto_now=True, verbose_name='Last modified')),
                ('date_of_creation', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('workspace', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='+',
                    to='core.workspace',
                )),
            ],
            options={
                'verbose_name': 'Product Family',
                'verbose_name_plural': 'Product Families',
                'db_table': 'products_productfamily',
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='product',
            name='product_family',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='products',
                to='products.productfamily',
                verbose_name='Product Family',
            ),
        ),
        # ── ProductVariant ───────────────────────────────────────────────
        migrations.CreateModel(
            name='ProductVariant',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('sku', models.CharField(max_length=200, verbose_name='SKU')),
                ('gtin', models.CharField(blank=True, max_length=14, null=True, verbose_name='GTIN')),
                ('mpn', models.CharField(blank=True, max_length=200, null=True, verbose_name='Manufacturer Part Number')),
                ('weight_kg', models.DecimalField(blank=True, decimal_places=4, max_digits=12, null=True, verbose_name='Weight (kg)')),
                ('dimensions_length_m', models.DecimalField(blank=True, decimal_places=4, max_digits=12, null=True, verbose_name='Length (m)')),
                ('dimensions_width_m', models.DecimalField(blank=True, decimal_places=4, max_digits=12, null=True, verbose_name='Width (m)')),
                ('dimensions_height_m', models.DecimalField(blank=True, decimal_places=4, max_digits=12, null=True, verbose_name='Height (m)')),
                ('axis_values', models.JSONField(blank=True, default=dict, verbose_name='Variant Axis Values')),
                ('last_modification', models.DateTimeField(auto_now=True, verbose_name='Last modified')),
                ('date_of_creation', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('product', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='variants',
                    to='products.product',
                    verbose_name='Product',
                )),
                ('workspace', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='+',
                    to='core.workspace',
                )),
            ],
            options={
                'verbose_name': 'Product Variant',
                'verbose_name_plural': 'Product Variants',
                'db_table': 'products_productvariant',
                'ordering': ['sku'],
            },
        ),
        # ── ProductTranslation ───────────────────────────────────────────
        migrations.CreateModel(
            name='ProductTranslation',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('language_code', models.CharField(max_length=10, verbose_name='Language Code')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('short_description', models.CharField(blank=True, max_length=500, null=True, verbose_name='Short Description')),
                ('long_description', models.TextField(blank=True, null=True, verbose_name='Long Description')),
                ('product', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='translations',
                    to='products.product',
                    verbose_name='Product',
                )),
                ('workspace', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='+',
                    to='core.workspace',
                )),
            ],
            options={
                'verbose_name': 'Product Translation',
                'verbose_name_plural': 'Product Translations',
                'db_table': 'products_producttranslation',
                'ordering': ['language_code'],
            },
        ),
        migrations.AddConstraint(
            model_name='producttranslation',
            constraint=models.UniqueConstraint(
                fields=('product', 'language_code'),
                name='unique_product_translation_per_language',
            ),
        ),
        # ── ProductMedia ─────────────────────────────────────────────────
        migrations.CreateModel(
            name='ProductMedia',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('media_type', models.CharField(
                    choices=[
                        ('image', 'Image'),
                        ('datasheet', 'Datasheet'),
                        ('certificate', 'Certificate'),
                    ],
                    max_length=32,
                    verbose_name='Media Type',
                )),
                ('object_key', models.CharField(max_length=1024, verbose_name='Object Storage Key')),
                ('last_modification', models.DateTimeField(auto_now=True, verbose_name='Last modified')),
                ('date_of_creation', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('product', models.ForeignKey(
                    blank=True,
                    null=True,
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='media_items',
                    to='products.product',
                    verbose_name='Product',
                )),
                ('variant', models.ForeignKey(
                    blank=True,
                    null=True,
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='media_items',
                    to='products.productvariant',
                    verbose_name='Product Variant',
                )),
                ('workspace', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='+',
                    to='core.workspace',
                )),
            ],
            options={
                'verbose_name': 'Product Media',
                'verbose_name_plural': 'Product Media',
                'db_table': 'products_productmedia',
                'ordering': ['id'],
            },
        ),
        migrations.AddConstraint(
            model_name='productmedia',
            constraint=models.CheckConstraint(
                condition=(
                    models.Q(('product__isnull', False), ('variant__isnull', True))
                    | models.Q(('product__isnull', True), ('variant__isnull', False))
                ),
                name='product_media_exactly_one_of_product_or_variant',
            ),
        ),
    ]
