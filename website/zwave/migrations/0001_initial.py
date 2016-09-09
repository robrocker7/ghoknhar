# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-08 23:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Switch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('device_id', models.IntegerField()),
                ('active', models.BooleanField(default=False)),
                ('value', models.IntegerField(blank=True, help_text=b'0-254 integer value if this is a dimmer switch.', null=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
