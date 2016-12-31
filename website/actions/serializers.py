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
    intendId = serializers.UUIDField()
    webhookUsed = serializers.CharField()
    webhookForSlotFillingUsed = serializers.CharField()
    intentName = serializers.CharField()

class GoogleActionResultSerializer(serializers.Serializer):
    source = serializers.CharField()
    resolvedQuery = serializers.CharField()
    action = serializers.CharField()
    actionIncomplete = serializers.CharField()
    parameters = serializers.JSONField()
    contexts = serializers.CharField()
    fulfillment = serializers.CharField()
    score = serializers.CharField()
    metadata = GoogleActionMetaSerializer()

class GoogleActionResponseSerializer(serializers.Serializer):
    speech = serializers.CharField()
    displayText = serializers.CharField()
    data = serializers.JSONField()
    contextOut = serializers.JSONField(many=True)
    source = "Johnson Castillo"

    def add_text_response(self, text):
        result = self.data
        result['speech'] = text
        result['displayText'] = text
        self.data = result


class GoogleActionRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    timestamp = serializers.CharField()
    status = GoogleActionStatusSerializer()
    sessionId = serializers.UUIDField()
    result = GoogleActionResultSerializer()
