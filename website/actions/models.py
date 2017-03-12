import json

from django.db import models
from django.contrib.auth.models import User


class ActionLog(models.Model):
    transaction_id = models.CharField(max_length=128)
    session_id = models.CharField(max_length=128)
    date_created = models.DateTimeField()
    status_code = models.IntegerField()
    fulfillment_payload = models.TextField()
    action_payload = models.TextField()


class ActionDatastore(models.Model):om
	user = models.ForeignKey(User)
	key = models.CharField(max_length=256, db_index=True)
	value = models.TextField()
	value_type = models.CharField(max_length=12)

    def get_value(self):
        if value_type == 'json':
            return json.loads(self.value)
        elif value_type == 'str':
            return str(self.value)
        return value