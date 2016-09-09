from rest_framework import serializers

from website.zwave.models import Switch

class SwitchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Switch