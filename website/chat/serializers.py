from rest_framework import serializers

from website.chat.models import Room, Message

class RoomSerializer(serializers.ModelSerializer):
    messages = serializers.StringRelatedField()
    class Meta:
        model = Room
        fields = ('name', 'slug', 'messages')

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('username', 'message', 'timestamp', 'room')