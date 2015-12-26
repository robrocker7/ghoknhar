# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-26 22:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zwave', '0004_instance_value'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommandClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_id', models.IntegerField(db_index=True)),
                ('instance_id', models.IntegerField(db_index=True)),
                ('command_class_id', models.CharField(choices=[['32', 'Basic'], ['38', 'SwitchMultilevel'], ['37', 'SwitchBinary'], ['43', 'SceneActivation'], ['115', 'PowerLevel'], ['134', 'Version'], ['94', 'ZWavePlusInfo'], ['90', 'DeviceResetLocally'], ['91', 'CentralScene'], ['133', 'Association'], ['129', 'Clock'], ['138', 'Time'], ['89', 'AssociationGroupInformation'], ['34', 'ApplicationStatus'], ['119', 'NodeNaming'], ['143', 'MultiCmd'], ['152', 'Security'], ['114', 'ManufacturerSpecific'], ['96', 'MultiChannel'], ['86', 'CRC16'], ['70', 'ClimateControlSchedule'], ['50', 'Meter'], ['112', 'Configuration'], ['49', 'SensorMultilevel'], ['39', 'SwitchAll']], db_index=True, max_length=255)),
                ('raw_data', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='instance',
            name='command_classes',
        ),
        migrations.RemoveField(
            model_name='instance',
            name='value',
        ),
        migrations.AddField(
            model_name='instance',
            name='generic_type',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='instance',
            name='specific_type',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
