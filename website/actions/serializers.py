import json
from rest_framework import serializers

class GoogleActionStatusSerializer(serializers.Serializer):
    code = serializers.IntegerField()
    errorType = serializers.CharField()

class GoogleActionFulfillmentMessageSerializer(serializers.Serializer):
    type = 0
    speech = serializers.CharField()


class GoogleActionFulfillmentSerializer(serializers.Serializer):
    speech = serializers.CharField()
    messages = GoogleActionFulfillmentMessageSerializer(many=True)

class GoogleActionMetaSerializer(serializers.Serializer):
    intentId = serializers.UUIDField()
    webhookUsed = serializers.CharField()
    webhookForSlotFillingUsed = serializers.CharField()
    intentName = serializers.CharField()

class GoogleActionResultSerializer(serializers.Serializer):
    source = serializers.CharField()
    resolvedQuery = serializers.CharField()
    action = serializers.CharField()
    actionIncomplete = serializers.CharField()
    parameters = serializers.JSONField()
    contexts = serializers.JSONField()
    fulfillment = serializers.JSONField()
    score = serializers.CharField()
    metadata = GoogleActionMetaSerializer()

class GoogleActionResponseSerializer(serializers.Serializer):
    speech = serializers.CharField()
    displayText = serializers.CharField()
    data = serializers.JSONField()
    contextOut = serializers.JSONField()
    source = "Johnson Castillo"

class GoogleActionRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    timestamp = serializers.CharField()
    status = GoogleActionStatusSerializer()
    sessionId = serializers.UUIDField()
    result = GoogleActionResultSerializer()


class GoogleCalendar(serializers.Serializer):
    """ 
    Google Calendar Resource
    Schema: https://developers.google.com/google-apps/calendar/v3/reference/calendarList#resource

    TODO: Add all attributes instead of just what I want
    """
    id = serializers.CharField()
    summary = serializers.CharField()
    accessRole = serializers.CharField()
