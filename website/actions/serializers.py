from rest_framework import serializers

class GoogleActionStatusSerializer(serializers.Serializer):
    code = serializers.IntegerField()
    errorType = serializers.CharField()

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


class GoogleActionResultSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    timestamp = serializers.CharField()
    status = GoogleActionStatusSerializer()
    sessionId = serializers.UUIDField()
    result = GoogleActionResultSerializer()
