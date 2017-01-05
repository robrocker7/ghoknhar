from django.db import models

class ActionLog(models.Model):
    transaction_id = models.CharField(max_length=128)
    session_id = models.CharField(max_length=128)
    date_created = models.DateTimeField()
    status_code = models.IntegerField()
    fulfillment_payload = models.TextField()
    action_payload = models.TextField()
