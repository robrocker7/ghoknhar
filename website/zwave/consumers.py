import json

from channels import Channel, Group

from website.zwave.models import Switch


def ws_message(message):
    try:
        zwave_event = json.loads(message.content['text'])
    except ValueError:
        return

    print zwave_event
    Switch.create_from_zwave_event(zwave_event)