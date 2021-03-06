# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-21 05:21
from __future__ import unicode_literals

from django.db import migrations, models
import select_multiple_field.models


class Migration(migrations.Migration):

    dependencies = [
        ('zwave', '0002_auto_20151219_2358'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='instance',
            name='device',
        ),
        migrations.AddField(
            model_name='instance',
            name='device_id',
            field=models.IntegerField(db_index=True, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='instance',
            name='instance_id',
            field=models.IntegerField(db_index=True, default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='device',
            name='device_id',
            field=models.IntegerField(db_index=True, unique=True),
        ),
        migrations.AlterField(
            model_name='instance',
            name='command_classes',
            field=select_multiple_field.models.SelectMultipleField(choices=[['32', 'Basic'], ['38', 'SwitchMultilevel'], ['37', 'SwitchBinary'], ['43', 'SceneActivation'], ['115', 'PowerLevel'], ['134', 'Version'], ['94', 'ZWavePlusInfo'], ['90', 'DeviceResetLocally'], ['91', 'CentralScene'], ['133', 'Association'], ['129', 'Clock'], ['138', 'Time'], ['89', 'AssociationGroupInformation'], ['34', 'ApplicationStatus'], ['119', 'NodeNaming'], ['143', 'MultiCmd'], ['152', 'Security'], ['114', 'ManufacturerSpecific'], ['96', 'MultiChannel'], ['86', 'CRC16'], ['70', 'ClimateControlSchedule'], ['50', 'Meter'], ['112', 'Configuration'], ['49', 'SensorMultilevel'], ['39', 'SwitchAll']], max_length=255),
        ),
    ]
