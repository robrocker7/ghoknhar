import json
from rest_framework import serializers

from .models import Device, Instance, CommandClass


class CommandClassSerializer(serializers.ModelSerializer):

    data = serializers.JSONField(source='raw_data', required=False)
    command_class = serializers.CharField(source='get_command_class_display')

    def to_representation(self, instance):
        ret = super(CommandClassSerializer, self).to_representation(instance)
        ret["data"] = json.loads(ret["data"])
        return ret

    def to_internal_value(self, instance):
        ret = super(CommandClassSerializer, self).to_internal_value(instance)
        ret["raw_data"] = json.dumps(ret["raw_data"])
        return ret

    def update(self, instance, validated_data):
        del validated_data['get_command_class_display']
        return super(CommandClassSerializer, self).update(instance, validated_data)

    class Meta:
        model = CommandClass
        fields = ('id',
                  'device_id',
                  'instance_id',
                  'command_class_id',
                  'command_class',
                  'value',
                  'data',)


class InstanceSerializer(serializers.ModelSerializer):
    command_classes = CommandClassSerializer(many=True,
                                             read_only=True,
                                             source='command_class_set')
    class Meta:
        model = Instance
        fields = ('id',
                  'device_id',
                  'instance_id',
                  'generic_type',
                  'specific_type',
                  'command_classes')


class DeviceSerializer(serializers.ModelSerializer):

    instances = InstanceSerializer(many=True,
                                   source='instance_set',
                                   read_only=True)
    class Meta:
        model = Device
        fields = ('id',
                  'name',
                  'active',
                  'device_id',
                  'instances')
