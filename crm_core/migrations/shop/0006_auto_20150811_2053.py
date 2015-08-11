# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20150527_1127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='description',
            field=models.CharField(max_length=2000, verbose_name='Description', blank=True),
            preserve_default=True,
        ),
    ]
