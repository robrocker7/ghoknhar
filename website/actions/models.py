from django import models

class ActionLog(models.Model):
	transaction_id = models.UUIDField()
	session_id = models.UUIDField()
	date_created = models.DateTimeField()
	status_code = models.IntegerField()
	fulfillment_payload = models.TextField()
	action_payload = models.TextField()