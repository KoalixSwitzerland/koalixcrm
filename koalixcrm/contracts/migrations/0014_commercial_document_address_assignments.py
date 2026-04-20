# -*- coding: utf-8 -*-
"""Replace MTI satellite models for CommercialDocument with assignment pattern.

Steps:
  1. CreateModel for CommercialDocumentAddressAssignment,
     CommercialDocumentPhoneAssignment, CommercialDocumentEmailAssignment.
  2. RunPython backfill from legacy crm_postaladdressforcommercialdocument /
     crm_phoneaddressforcommercialdocument / crm_emailaddressforcommercialdocument
     into the new value + assignment tables.  Reverse is a no-op (data only).
  3. DeleteModel for the three legacy satellites.
"""
import django.db.models.deletion
from django.db import migrations, models


def backfill_document_assignments(apps, schema_editor):
    Workspace = apps.get_model('core', 'Workspace')
    Address = apps.get_model('contacts', 'Address')
    PhoneNumber = apps.get_model('contacts', 'PhoneNumber')
    PartyEmail = apps.get_model('contacts', 'PartyEmail')
    CommercialDocumentAddressAssignment = apps.get_model(
        'contract_object_management', 'CommercialDocumentAddressAssignment'
    )
    CommercialDocumentPhoneAssignment = apps.get_model(
        'contract_object_management', 'CommercialDocumentPhoneAssignment'
    )
    CommercialDocumentEmailAssignment = apps.get_model(
        'contract_object_management', 'CommercialDocumentEmailAssignment'
    )

    ws, _ = Workspace.objects.get_or_create(
        name='Default Workspace',
        defaults={'is_active': True},
    )

    PostalAddressForCommercialDocument = apps.get_model(
        'contract_object_management', 'PostalAddressForCommercialDocument'
    )
    for row in PostalAddressForCommercialDocument.objects.select_related('commercial_document').iterator():
        addr = Address.objects.create(
            workspace=ws,
            address_line_1=row.address_line_1,
            address_line_2=row.address_line_2,
            address_line_3=row.address_line_3,
            address_line_4=row.address_line_4,
            zip_code=str(row.zip_code) if row.zip_code is not None else None,
            town=row.town,
            state=row.state,
            country=row.country,
            subdivision_code=row.subdivision_code,
        )
        CommercialDocumentAddressAssignment.objects.create(
            workspace=ws,
            document=row.commercial_document,
            address=addr,
            purpose='primary',
            is_primary=True,
        )

    PhoneAddressForCommercialDocument = apps.get_model(
        'contract_object_management', 'PhoneAddressForCommercialDocument'
    )
    for row in PhoneAddressForCommercialDocument.objects.select_related('commercial_document').iterator():
        phone = PhoneNumber.objects.create(
            workspace=ws,
            phone_e164=row.phone,
        )
        CommercialDocumentPhoneAssignment.objects.create(
            workspace=ws,
            document=row.commercial_document,
            phone_number=phone,
            purpose='primary',
            is_primary=True,
        )

    EmailAddressForCommercialDocument = apps.get_model(
        'contract_object_management', 'EmailAddressForCommercialDocument'
    )
    for row in EmailAddressForCommercialDocument.objects.select_related('commercial_document').iterator():
        email = PartyEmail.objects.create(
            workspace=ws,
            email=row.email,
        )
        CommercialDocumentEmailAssignment.objects.create(
            workspace=ws,
            document=row.commercial_document,
            email=email,
            purpose='primary',
            is_primary=True,
        )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('contract_object_management', '0013_contract_address_assignments'),
        ('contacts', '0011_workspace_scoping'),
        ('core', '0006_pdf_export_process_workspace'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommercialDocumentAddressAssignment',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('workspace', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='+',
                    to='core.workspace',
                )),
                ('document', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='address_assignments',
                    to='contract_object_management.commercialdocument',
                    verbose_name='Commercial Document',
                )),
                ('address', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='commercial_document_assignments',
                    to='contacts.address',
                    verbose_name='Address',
                )),
                ('purpose', models.CharField(
                    choices=[
                        ('primary', 'Primary'),
                        ('billing', 'Billing'),
                        ('shipping', 'Shipping'),
                        ('legal', 'Legal / registered seat'),
                        ('visit', 'Visiting'),
                        ('other', 'Other'),
                    ],
                    max_length=16,
                    verbose_name='Purpose',
                )),
                ('is_primary', models.BooleanField(default=False, verbose_name='Is primary')),
                ('valid_from', models.DateField(blank=True, null=True, verbose_name='Valid from')),
                ('valid_to', models.DateField(blank=True, null=True, verbose_name='Valid to')),
            ],
            options={
                'verbose_name': 'Commercial Document Address Assignment',
                'verbose_name_plural': 'Commercial Document Address Assignments',
                'db_table': 'crm_commercialdocumentaddressassignment',
                'app_label': 'contract_object_management',
            },
        ),
        migrations.CreateModel(
            name='CommercialDocumentPhoneAssignment',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('workspace', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='+',
                    to='core.workspace',
                )),
                ('document', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='phone_assignments',
                    to='contract_object_management.commercialdocument',
                    verbose_name='Commercial Document',
                )),
                ('phone_number', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='commercial_document_assignments',
                    to='contacts.phonenumber',
                    verbose_name='Phone number',
                )),
                ('purpose', models.CharField(
                    choices=[
                        ('primary', 'Primary'),
                        ('billing', 'Billing'),
                        ('shipping', 'Shipping'),
                        ('legal', 'Legal / registered seat'),
                        ('visit', 'Visiting'),
                        ('other', 'Other'),
                    ],
                    max_length=16,
                    verbose_name='Purpose',
                )),
                ('is_primary', models.BooleanField(default=False, verbose_name='Is primary')),
                ('valid_from', models.DateField(blank=True, null=True, verbose_name='Valid from')),
                ('valid_to', models.DateField(blank=True, null=True, verbose_name='Valid to')),
            ],
            options={
                'verbose_name': 'Commercial Document Phone Assignment',
                'verbose_name_plural': 'Commercial Document Phone Assignments',
                'db_table': 'crm_commercialdocumentphoneassignment',
                'app_label': 'contract_object_management',
            },
        ),
        migrations.CreateModel(
            name='CommercialDocumentEmailAssignment',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('workspace', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='+',
                    to='core.workspace',
                )),
                ('document', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='email_assignments',
                    to='contract_object_management.commercialdocument',
                    verbose_name='Commercial Document',
                )),
                ('email', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='commercial_document_assignments',
                    to='contacts.partyemail',
                    verbose_name='Email',
                )),
                ('purpose', models.CharField(
                    choices=[
                        ('primary', 'Primary'),
                        ('billing', 'Billing'),
                        ('shipping', 'Shipping'),
                        ('legal', 'Legal / registered seat'),
                        ('visit', 'Visiting'),
                        ('other', 'Other'),
                    ],
                    max_length=16,
                    verbose_name='Purpose',
                )),
                ('is_primary', models.BooleanField(default=False, verbose_name='Is primary')),
                ('valid_from', models.DateField(blank=True, null=True, verbose_name='Valid from')),
                ('valid_to', models.DateField(blank=True, null=True, verbose_name='Valid to')),
            ],
            options={
                'verbose_name': 'Commercial Document Email Assignment',
                'verbose_name_plural': 'Commercial Document Email Assignments',
                'db_table': 'crm_commercialdocumentemailassignment',
                'app_label': 'contract_object_management',
            },
        ),
        migrations.RunPython(backfill_document_assignments, noop),
        migrations.DeleteModel(name='PostalAddressForCommercialDocument'),
        migrations.DeleteModel(name='PhoneAddressForCommercialDocument'),
        migrations.DeleteModel(name='EmailAddressForCommercialDocument'),
    ]
