from django.db import models


class Switch(models.Model):
    name = models.CharField(max_length=128)
    device_id = models.IntegerField()
    active = models.BooleanField(default=False)
    value = models.IntegerField(null=True, blank=True,
        help_text="0-254 integer value if this is a dimmer switch.")
    last_update = models.DateTimeField(auto_now=True)

    @staticmethod
    def create_from_zwave_event(e):
        did = e.pop('device_id')
        params = {
            'name': e.get('name', 'Device {0}'.format(did)),
            'active': e['types']['switch']['active']
        }
        s, created = Switch.objects.update_or_create(device_id=did, defaults=params)