# -*- coding: utf-8 -*-
"""
Replace the three MTI satellite models (UserExtensionPostalAddress,
UserExtensionPhoneAddress, UserExtensionEmailAddress) with three assignment
models that reuse the Party-pattern value types from koalixcrm.contacts.
"""
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def backfill_assignments(apps, schema_editor):
    Workspace = apps.get_model('core', 'Workspace')
    ws, _ = Workspace.objects.get_or_create(
        name='Default Workspace',
        defaults={'is_active': True},
    )

    Address = apps.get_model('contacts', 'Address')
    PhoneNumber = apps.get_model('contacts', 'PhoneNumber')
    PartyEmail = apps.get_model('contacts', 'PartyEmail')
    UserAddressAssignment = apps.get_model('djangoUserExtension', 'UserAddressAssignment')
    UserPhoneAssignment = apps.get_model('djangoUserExtension', 'UserPhoneAssignment')
    UserEmailAssignment = apps.get_model('djangoUserExtension', 'UserEmailAssignment')
    UserExtensionPostalAddress = apps.get_model('djangoUserExtension', 'UserExtensionPostalAddress')
    UserExtensionPhoneAddress = apps.get_model('djangoUserExtension', 'UserExtensionPhoneAddress')
    UserExtensionEmailAddress = apps.get_model('djangoUserExtension', 'UserExtensionEmailAddress')

    for legacy in UserExtensionPostalAddress.objects.select_related('userExtension').all():
        address = Address.objects.create(
            workspace=ws,
            address_line_1=legacy.address_line_1,
            address_line_2=legacy.address_line_2,
            address_line_3=legacy.address_line_3,
            address_line_4=legacy.address_line_4,
            zip_code=str(legacy.zip_code) if legacy.zip_code is not None else None,
            town=legacy.town,
            state=legacy.state,
            country=legacy.country,
            subdivision_code=legacy.subdivision_code,
        )
        UserAddressAssignment.objects.create(
            workspace=ws,
            user=legacy.userExtension.user,
            address=address,
            purpose='primary',
            is_primary=True,
        )

    for legacy in UserExtensionPhoneAddress.objects.select_related('userExtension').all():
        phone_number = PhoneNumber.objects.create(
            workspace=ws,
            phone_e164=legacy.phone,
        )
        UserPhoneAssignment.objects.create(
            workspace=ws,
            user=legacy.userExtension.user,
            phone_number=phone_number,
            purpose='primary',
            is_primary=True,
        )

    for legacy in UserExtensionEmailAddress.objects.select_related('userExtension').all():
        party_email = PartyEmail.objects.create(
            workspace=ws,
            email=legacy.email,
        )
        UserEmailAssignment.objects.create(
            workspace=ws,
            user=legacy.userExtension.user,
            email=party_email,
            purpose='primary',
            is_primary=True,
        )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('djangoUserExtension', '0004_workspace_scoping'),
        ('contacts', '0011_workspace_scoping'),
        ('core', '0006_pdf_export_process_workspace'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAddressAssignment',
            fields=[
                ('workspace', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='+',
                    to='core.workspace',
                )),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='address_assignments',
                    to=settings.AUTH_USER_MODEL,
                    verbose_name='User',
                )),
                ('address', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='user_assignments',
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
                'verbose_name': 'Address assignment for User',
                'verbose_name_plural': 'Address assignments for User',
                'app_label': 'djangoUserExtension',
            },
        ),
        migrations.CreateModel(
            name='UserPhoneAssignment',
            fields=[
                ('workspace', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='+',
                    to='core.workspace',
                )),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='phone_assignments',
                    to=settings.AUTH_USER_MODEL,
                    verbose_name='User',
                )),
                ('phone_number', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='user_assignments',
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
                'verbose_name': 'Phone assignment for User',
                'verbose_name_plural': 'Phone assignments for User',
                'app_label': 'djangoUserExtension',
            },
        ),
        migrations.CreateModel(
            name='UserEmailAssignment',
            fields=[
                ('workspace', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='+',
                    to='core.workspace',
                )),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='email_assignments',
                    to=settings.AUTH_USER_MODEL,
                    verbose_name='User',
                )),
                ('email', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='user_assignments',
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
                'verbose_name': 'Email assignment for User',
                'verbose_name_plural': 'Email assignments for User',
                'app_label': 'djangoUserExtension',
            },
        ),

        migrations.RunPython(backfill_assignments, noop),

        migrations.DeleteModel(name='UserExtensionPostalAddress'),
        migrations.DeleteModel(name='UserExtensionPhoneAddress'),
        migrations.DeleteModel(name='UserExtensionEmailAddress'),
    ]
