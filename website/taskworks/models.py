from django.auth.contrib.models import User
from django.db import models

from jsonfield import JSONField


class Task(models.Model):
    TYPES = (
        ('light', 'LightSwitch'),
        ('text', 'Text'),
        ('play', 'PlaySound'),
        ('api', 'API'),
    )

    name = models.CharField(max_length=128)
    type = models.CharField(max_length=12, choices=TYPES)
    attributes = models.JSONField(null=True, blank=True)


class Context(models.Model):
    """
    Task Context

    The context of the task:
        - User (if any) the task is associated to.
        - Location
         - BLE, WIFI Connected, GPS
    """

    TYPES = (
        ('day', 'Day')<
        ('event', 'Event'),
        ('location', 'Location'),
        ('time', 'Time'),
    )

    user = models.ForeignKey(User, blank=True, null=True)
    type = models.CharField(max_length=12, choices=TYPES)
    task = models.ForeignKey(Task, blank=True, null=True)
