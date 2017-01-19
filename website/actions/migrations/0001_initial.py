# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-01-05 22:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ActionLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.CharField(max_length=128)),
                ('session_id', models.CharField(max_length=128)),
                ('date_created', models.DateTimeField()),
                ('status_code', models.IntegerField()),
                ('fulfillment_payload', models.TextField()),
                ('action_payload', models.TextField()),
            ],
        ),
    ]