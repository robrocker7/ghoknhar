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


class GoogleActionResultSerializer(serializers.Serializer):
    source = serializers.CharField()
    resolvedQuery = serializers.CharField()
    action = serializers.CharField()
    actionIncomplete = serializers.CharField()
    parameters = serializers.CharField()
    contexts = serializers.CharField()
    fulfillment = serializers.CharField()
    score = serializers.CharField()
    metadata = serializers.CharField()

class GoogleActionResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    timestamp = serializers.CharField()
    status = GoogleActionStatusSerializer()
    sessionId = serializers.UUIDField()
    result = GoogleActionResultSerializer()

    def add_text_response(self, text):
        message = GoogleActionFulfillmentMessageSerializer(
            speech=text)
        fulfillment = GoogleActionFulfillmentSerializer(
            speech=text, messages=[message,])
        self.result.fulfillment=fulfillment


class GoogleActionRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    timestamp = serializers.CharField()
    status = GoogleActionStatusSerializer()
    sessionId = serializers.UUIDField()
    result = GoogleActionResultSerializer()
