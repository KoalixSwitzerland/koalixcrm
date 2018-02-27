# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-21 13:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0029_auto_20180220_2348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='people',
            field=models.ManyToManyField(blank=True, through='crm.CustomerPersonAssociation', to='crm.Person'),
        ),
        migrations.AlterField(
            model_name='person',
            name='customers',
            field=models.ManyToManyField(blank=True, through='crm.CustomerPersonAssociation', to='crm.Customer'),
        ),
    ]