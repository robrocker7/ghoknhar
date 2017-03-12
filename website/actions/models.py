import json

from django.db import models
from django.contrib.auth.models import User
from django.template import Context, Template


class ActionLog(models.Model):
    transaction_id = models.CharField(max_length=128)
    session_id = models.CharField(max_length=128)
    date_created = models.DateTimeField()
    status_code = models.IntegerField()
    fulfillment_payload = models.TextField()
    action_payload = models.TextField()


class ActionDatastore(models.Model):
    user = models.ForeignKey(User)
    key = models.CharField(max_length=256, db_index=True)
    value = models.TextField()
    value_type = models.CharField(max_length=12)

    def get_value(self):
        if self.value_type == 'json':
            return json.loads(self.value)
        elif self.value_type == 'str':
            return str(self.value)
        return self.value

    def populate_tokens(self, params):
        t = Template(self.value)
        c = Context(params)
        self.value = t.render(c)
        return self.get_value()
