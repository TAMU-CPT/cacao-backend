# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-03-23 17:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_merge_20170228_1759'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='gaf',
            unique_together=set([('db', 'go_id', 'notes', 'evidence_code', 'gene')]),
        ),
    ]
