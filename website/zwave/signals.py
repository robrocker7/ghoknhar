from django.dispatch import receiver
from django.db.models.signals import post_save
from channels import Group
import json

from website.zwave.models import Switch

@receiver(post_save, sender=Switch, dispatch_uid="update_switch_item")
def send_update(sender, instance, **kwargs):
    print "object updated"
    Group("zwave").send({
        "text": json.dumps({
            "id": instance.device_id,
            "active": instance.active
        })
    })