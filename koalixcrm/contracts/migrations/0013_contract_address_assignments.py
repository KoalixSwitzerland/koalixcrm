# -*- coding: utf-8 -*-
"""Replace MTI satellite models for Contract with assignment pattern.

Steps:
  1. CreateModel for ContractAddressAssignment, ContractPhoneAssignment,
     ContractEmailAssignment.
  2. RunPython backfill from legacy crm_postaladdressforcontract /
     crm_phoneaddressforcontract / crm_emailaddressforcontract into the new
     value + assignment tables.  Reverse is a no-op (data only).
  3. DeleteModel for the three legacy satellites.
"""
import django.db.models.deletion
from django.db import migrations, models


def backfill_contract_assignments(apps, schema_editor):
    Workspace = apps.get_model('core', 'Workspace')
    Address = apps.get_model('contacts', 'Address')
    PhoneNumber = apps.get_model('contacts', 'PhoneNumber')
    PartyEmail = apps.get_model('contacts', 'PartyEmail')
    ContractAddressAssignment = apps.get_model('contract_object_management', 'ContractAddressAssignment')
    ContractPhoneAssignment = apps.get_model('contract_object_management', 'ContractPhoneAssignment')
    ContractEmailAssignment = apps.get_model('contract_object_management', 'ContractEmailAssignment')

    ws, _ = Workspace.objects.get_or_create(
        name='Default Workspace',
        defaults={'is_active': True},
    )

    PostalAddressForContract = apps.get_model('contract_object_management', 'PostalAddressForContract')
    for row in PostalAddressForContract.objects.select_related('contract').iterator():
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
        ContractAddressAssignment.objects.create(
            workspace=ws,
            contract=row.contract,
            address=addr,
            purpose='primary',
            is_primary=True,
        )

    PhoneAddressForContract = apps.get_model('contract_object_management', 'PhoneAddressForContract')
    for row in PhoneAddressForContract.objects.select_related('contract').iterator():
        phone = PhoneNumber.objects.create(
            workspace=ws,
            phone_e164=row.phone,
        )
        ContractPhoneAssignment.objects.create(
            workspace=ws,
            contract=row.contract,
            phone_number=phone,
            purpose='primary',
            is_primary=True,
        )

    EmailAddressForContract = apps.get_model('contract_object_management', 'EmailAddressForContract')
    for row in EmailAddressForContract.objects.select_related('contract').iterator():
        email = PartyEmail.objects.create(
            workspace=ws,
            email=row.email,
        )
        ContractEmailAssignment.objects.create(
            workspace=ws,
            contract=row.contract,
            email=email,
            purpose='primary',
            is_primary=True,
        )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('contract_object_management', '0012_position_tax_rate'),
        ('contacts', '0011_workspace_scoping'),
        ('core', '0006_pdf_export_process_workspace'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContractAddressAssignment',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('workspace', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='+',
                    to='core.workspace',
                )),
                ('contract', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='address_assignments',
                    to='contract_object_management.contract',
                    verbose_name='Contract',
                )),
                ('address', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='contract_assignments',
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
                'verbose_name': 'Contract Address Assignment',
                'verbose_name_plural': 'Contract Address Assignments',
                'db_table': 'crm_contractaddressassignment',
                'app_label': 'contract_object_management',
            },
        ),
        migrations.CreateModel(
            name='ContractPhoneAssignment',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('workspace', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='+',
                    to='core.workspace',
                )),
                ('contract', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='phone_assignments',
                    to='contract_object_management.contract',
                    verbose_name='Contract',
                )),
                ('phone_number', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='contract_assignments',
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
                'verbose_name': 'Contract Phone Assignment',
                'verbose_name_plural': 'Contract Phone Assignments',
                'db_table': 'crm_contractphoneassignment',
                'app_label': 'contract_object_management',
            },
        ),
        migrations.CreateModel(
            name='ContractEmailAssignment',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('workspace', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='+',
                    to='core.workspace',
                )),
                ('contract', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='email_assignments',
                    to='contract_object_management.contract',
                    verbose_name='Contract',
                )),
                ('email', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='contract_assignments',
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
                'verbose_name': 'Contract Email Assignment',
                'verbose_name_plural': 'Contract Email Assignments',
                'db_table': 'crm_contractemailassignment',
                'app_label': 'contract_object_management',
            },
        ),
        migrations.RunPython(backfill_contract_assignments, noop),
        migrations.DeleteModel(name='PostalAddressForContract'),
        migrations.DeleteModel(name='PhoneAddressForContract'),
        migrations.DeleteModel(name='EmailAddressForContract'),
    ]
