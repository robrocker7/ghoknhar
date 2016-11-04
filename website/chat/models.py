from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Room(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(unique=True)

class Message(models.Model):
    room  = models.ForeignKey(Room, related_name='messages')
    user_id = models.IntegerField(blank=True, null=True)
    username = models.CharField(max_length=128)
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    def __unicode__(self):
        return u'{0}: {1}'.format(self.username, self.message)