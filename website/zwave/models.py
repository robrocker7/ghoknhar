import os
import json
import re

from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from website.zwave import constants
from .coms import ZWaveController
"""
NOTES:
 - each device has an instances and data
    - instances = list of ways to get data from a device
        - instance has data and command classes
            - data: describes the object
            - command classes: list of dicts. key = commandid
                - command: data, name
                    - data:
                    - name: name of command
    - data:
"""


class DeviceManager(models.Manager):

    CONSTANT_FILES = (
            'command_classes',
        )

    def get_constant_attr_name(self, constant):
        return '{0}.{1}'.format(constant, constant.upper())

    def get_constant_attr(self, constant):
        return getattr(constants, self.get_constant_attr_name(constant), None)

    def get_constants_from_file(self, constant):
        fp = self.get_constant_filepath(constant)
        f = open(fp, 'r')
        f_data = f.read()
        f_regex = re.compile('{0} = (.*)'.format(constant.upper()))
        f_matches = f_regex.match(f_data)
        return json.loads(f_matches.groups()[0])

    def get_constant_filepath(self, constant):
        return os.path.join(settings.BASE_DIR,
                            'zwave',
                            'constants',
                            '{0}.py'.format(constant))

    def check_for_constants(self):
        """ Create constant files if they do not exist. """
        for cf in self.CONSTANT_FILES:
            cf_path = self.get_constant_filepath(cf)
            if not os.path.isfile(cf_path):
                f = open(cf_path, 'w')
                f.close()

    def sync_data(self, sync_constants=False):
        """ Sync the data from the ZWaveController. """
        self.check_for_constants()

        devices = []
        instances = []
        command_classes = []
        con = ZWaveController(ip=settings.ZWAVE_SETTINGS['DOMAIN'],
                              port=settings.ZWAVE_SETTINGS['PORT'])

        for did, device in con.devices.iteritems():
            # TODO: check if device exists here and change logic
            # but for now we're going to dump everythign and rewrite it
            p_devices, p_instances, p_classes = Device.prepare_from_zwave_device(
                did, device, sync_constants=sync_constants)
            devices.append(p_devices)
            instances += p_instances
            command_classes += p_classes

        Instance.objects.all().delete()
        Device.objects.all().delete()
        CommandClass.objects.all().delete()

        Instance.objects.bulk_create(instances)
        Device.objects.bulk_create(devices)
        CommandClass.objects.bulk_create(command_classes)
        print "Done"
        # print devices
        # print instances

    def update_constants_file(self, constant, value_tuple):
        constant_attr = self.get_constant_attr(constant)
        if constant_attr is not None:  # Combine and dedupe
            value_tuple = constant_attr + list(set(value_tuple) -
                                               set(constant_attr))

        # TODO: Make this smarter so that the values only update if different
        print "Setting new Attributes -> {0}".format(value_tuple)
        setattr(constants, self.get_constant_attr_name(constant), value_tuple)

        # Save the file
        cf_path = self.get_constant_filepath(constant)
        f = open(cf_path, 'w')
        f.write("{0} = {1}".format(constant.upper(), json.dumps(value_tuple)))
        f.close()
        return


class Device(models.Model):
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=False)

    device_id = models.IntegerField(db_index=True, unique=True)

    objects = DeviceManager()

    @property
    def instance_set(self):
        return Instance.objects.filter(device_id=self.device_id)

    @classmethod
    def prepare_from_zwave_device(cls, did, device, sync_constants=False):
        """
        Create the zwave device object and do not save it.

        Return Device and Instance objects.
        """
        d = cls()
        d.name = device['data']['givenName']['value']
        d.device_id = int(did)

        instances = []
        command_classes = []
        for iid, instance in device['instances'].iteritems():
            if sync_constants:
                command_classes_tuple = [(cid, c['name']) for cid, c in instance['commandClasses'].iteritems()]
                cls.objects.update_constants_file('command_classes',
                                                  command_classes_tuple)

            instances.append(Instance.prepare_from_zwave_instance(
                iid, d.device_id, instance))

            command_classes += CommandClass.prepare_from_zwave_classes(
                instance['commandClasses'], d.device_id, iid)


        return d, instances, command_classes

    def __unicode__(self):
        return '{0} -> Active: {1}'.format(self.name, self.active)


class Instance(models.Model):
    device_id = models.IntegerField(db_index=True)

    instance_id = models.IntegerField(db_index=True)

    generic_type = models.IntegerField(blank=True, null=True)
    specific_type = models.IntegerField(blank=True, null=True)

    @property
    def command_class_set(self):
        return CommandClass.objects.filter(instance_id=self.instance_id)

    @classmethod
    def prepare_from_zwave_instance(cls, iid, did, instance):
        i = cls()
        i.instance_id = int(iid)
        i.device_id = int(did)

        i.generic_type = int(instance['data']['genericType']['value'])
        i.specific_type = int(instance['data']['specificType']['value'])
        return i

    def __unicode__(self):
        return '{0}[{1}]'.format(self.device_id, self.instance_id)


class CommandClass(models.Model):
    COMMAND_CHOICES = Device.objects.get_constants_from_file('command_classes')

    device_id = models.IntegerField(db_index=True)
    instance_id = models.IntegerField(db_index=True)
    command_class_id = models.CharField(db_index=True,
                                        max_length=255,
                                        choices=COMMAND_CHOICES)

    raw_data = models.TextField(blank=True, null=True)

    @classmethod
    def prepare_from_zwave_classes(cls, classes, did, iid):
        result = []
        # print classes
        for ccid, ccdata in classes.iteritems():
            c = CommandClass(device_id=did,
                             instance_id=iid,
                             command_class_id=ccid,
                             raw_data=json.dumps(ccdata))
            result.append(c)
        return result

    @property
    def get_command_class_display(self):
        try:
            return dict(self.COMMAND_CHOICES)[self.command_class_id]
        except:
            return 'ERROR'

    def __unicode__(self):
        return '{3}(device.{0} instance.{1} class.{2})'.format(
            self.device_id, self.instance_id, self.command_class_id,
            self.get_command_class_display)


@receiver(post_save, sender=CommandClass)
def device_post_save(sender, **kwargs):
    cc = kwargs['instance']
    con = ZWaveController(ip=settings.ZWAVE_SETTINGS['DOMAIN'],
                          port=settings.ZWAVE_SETTINGS['PORT'])
    con.run_command(cc.device_id, cc.instance_id, cc.command_class_id, cc.value)
