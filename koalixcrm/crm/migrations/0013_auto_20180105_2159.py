# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-05 21:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('djangoUserExtension', '0004_auto_20171210_2126'),
        ('crm', '0012_auto_20180105_1840'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchaseconfirmation',
            name='status',
        ),
        migrations.RemoveField(
            model_name='purchaseconfirmation',
            name='valid_until',
        ),
        migrations.AddField(
            model_name='deliverynote',
            name='derived_from_quote',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.Quote'),
        ),
        migrations.AddField(
            model_name='deliverynote',
            name='tracking_reference',
            field=models.CharField(blank=True, max_length=100, verbose_name='Tracking Reference'),
        ),
        migrations.AddField(
            model_name='paymentreminder',
            name='payable_until',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='To pay until'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='paymentreminder',
            name='payment_bank_reference',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Payment Bank Reference'),
        ),
        migrations.AddField(
            model_name='purchaseconfirmation',
            name='derived_from_quote',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.Quote'),
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='template_set',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='djangoUserExtension.DocumentTemplate', verbose_name='Referred Template'),
        ),
    ]
