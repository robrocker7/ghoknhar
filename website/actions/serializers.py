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
    parameters = serializers.CharField()
    contexts = serializers.CharField()
    fulfillment = serializers.CharField()
    score = serializers.CharField()
    metadata = GoogleActionMetaSerializer()

class GoogleActionResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    timestamp = serializers.CharField()
    status = GoogleActionStatusSerializer()
    sessionId = serializers.UUIDField()
    result = GoogleActionResultSerializer()

    def add_text_response(self, text):
        result = self.data['result']
        result['fulfillment'] = {
            'speech': text,
            'messages': [{
                'type': 0,
                'speech': text
            }]
        }
        self.data['result'] = result


class GoogleActionRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    timestamp = serializers.CharField()
    status = GoogleActionStatusSerializer()
    sessionId = serializers.UUIDField()
    result = GoogleActionResultSerializer()
