# Generated migration for koalixcrm contacts app (split from crm)

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


from koalixcrm.migration_utils import CreateModelIfNotExists, AddFieldIfNotExists


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contacts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        AddFieldIfNotExists(
            model_name='person',
            name='companies',
            field=models.ManyToManyField(blank=True, through='contacts.ContactPersonAssociation', to='contacts.contact', verbose_name='Works at'),
        ),
        AddFieldIfNotExists(
            model_name='contactpersonassociation',
            name='person',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contact_association', to='contacts.person'),
        ),
        AddFieldIfNotExists(
            model_name='callforcontact',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contacts.contact'),
        ),
        AddFieldIfNotExists(
            model_name='callforcontact',
            name='cperson',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contacts.person', verbose_name='Person'),
        ),
        AddFieldIfNotExists(
            model_name='visitforcontact',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contacts.contact'),
        ),
        AddFieldIfNotExists(
            model_name='visitforcontact',
            name='cperson',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contacts.person', verbose_name='Person'),
        ),
        AddFieldIfNotExists(
            model_name='visitforcontact',
            name='ref_call',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contacts.callforcontact', verbose_name='Reference Call'),
        ),
        AddFieldIfNotExists(
            model_name='customer',
            name='default_customer_billing_cycle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contacts.customerbillingcycle', verbose_name='Default Billing Cycle'),
        ),
        AddFieldIfNotExists(
            model_name='customer',
            name='is_member_of',
            field=models.ManyToManyField(blank=True, to='contacts.customergroup', verbose_name='Is member of'),
        ),
        AddFieldIfNotExists(
            model_name='emailaddressforcontact',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contacts.contact'),
        ),
        CreateModelIfNotExists(
            name='PhoneAddressForContact',
            fields=[
                ('phoneaddress_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='contacts.phoneaddress')),
                ('purpose', models.CharField(choices=[('H', 'Private'), ('O', 'Business'), ('P', 'Mobile Private'), ('B', 'Mobile Business')], max_length=1, verbose_name='Purpose')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contacts.contact')),
            ],
            options={
                'verbose_name': 'Phone Address For Contact',
                'verbose_name_plural': 'Phone Address For Contact',
                'db_table': 'crm_phoneaddressforcontact',
            },
            bases=('contacts.phoneaddress',),
        ),
        CreateModelIfNotExists(
            name='PostalAddressForContact',
            fields=[
                ('postaladdress_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='contacts.postaladdress')),
                ('purpose', models.CharField(choices=[('H', 'Private'), ('O', 'Business'), ('P', 'Mobile Private'), ('B', 'Mobile Business')], max_length=1, verbose_name='Purpose')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contacts.contact')),
            ],
            options={
                'verbose_name': 'Postal Address For Contact',
                'verbose_name_plural': 'Postal Address For Contact',
                'db_table': 'crm_postaladdressforcontact',
            },
            bases=('contacts.postaladdress',),
        ),
    ]
