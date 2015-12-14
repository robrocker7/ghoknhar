from django.db import models

from .constants import DEVICE_TYPES
"""
NOTES:
 - each device has an instances and data
    - instances = list of ways to get data from a device
        - instance has data and command classes
            - data: describes the object
            - command classes: list of dicts. key = commandid
                - command: data, name
                    - data:
                    - name: name of command
    - data:
"""

class Device(models.Model):
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=False)

    # ZWave Meta Data
    device_type = models.CharField(max_length=16, choices=DEVICE_TYPES)
    device_id = models.IntegerField()

    # TODO: Add command to sync the devices data
    def sync_with_device(self):
        pass

    def __unicode__(self):
        return '{0} -> Active: {1}'.format(self.name, self.active)
