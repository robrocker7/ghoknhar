from django.db import models

class ActionLog(models.Model):
	transaction_id = models.CharField()
	session_id = models.CharField()
	date_created = models.DateTimeField()
	status_code = models.IntegerField()
	fulfillment_payload = models.TextField()
	action_payload = models.TextField()
