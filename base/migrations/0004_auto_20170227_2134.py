# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-02-27 21:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_auto_20160901_1736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organism',
            name='common_name',
            field=models.CharField(max_length=128, unique=True),
        ),
    ]
