# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-03-13 14:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actions', '0002_actiondatastore'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actiondatastore',
            name='key',
            field=models.CharField(db_index=True, max_length=256),
        ),
    ]